import requests
import json
from dateutil.relativedelta import relativedelta
import io, json, re, unicodedata, time
from datetime import datetime, date
from calendar import monthrange
import boto3
from botocore.config import Config
from apps import config

s3_client = boto3.client(
    's3',
    endpoint_url="http://localhost:9002",  # API do MinIO
    aws_access_key_id="minioadmin",        # usuário definido no docker-compose
    aws_secret_access_key="minioadmin",    # senha definida no docker-compose
    region_name="us-east-1"                # região dummy (MinIO não exige)
)


#Extraindo todos os códigos de municipios do Brasil pela API do IBGE para buscar na API do Portal da Transparencia os valores recebidos pelo Bolsa Familia
def codigos_ibge(URL_API_IBGE):
    response = requests.get(URL_API_IBGE)
    municipios = response.json()

    codigos_municipios = [str(m["id"]) for m in municipios]
    return codigos_municipios

#Recebe os parametros de datas para a consulta na API do Portal da Transparencia
def datas(DATA_INICIO: str, DATA_FIM: str):
    datas = []
    start = datetime.fromisoformat(DATA_INICIO[0:4] + '-' + DATA_INICIO[4:6] + '-01').date()
    end = datetime.fromisoformat(DATA_FIM[0:4] + '-' + DATA_FIM[4:6] + '-01').date()
    while start <= end:
        datas.append(start.strftime("%Y%m"))
        start += relativedelta(months=1)
    return datas

#Recebe o nome dos Municipios do arquivo JSON e faz tratamentos para remover acentos, espaços em branco e deixa tudo minusculo
def normalizar_municipio(mun_ext: str):
    if not mun_ext:
        return ""
    mun_sem_acentos = ''.join(
        c for c in unicodedata.normalize('NFKD', mun_ext)
        if not unicodedata.combining(c)
    )
    mun_sem_acentos = mun_sem_acentos.lower()
    nome_municipio = re.sub(r'[^a-z0-9]', '', mun_sem_acentos)

    return nome_municipio


#Recebe o nome do municipio e prepara o nome final do arquivo já particionando pro ANO/MES
def nome_arquivo_output(rec: dict, yyyymm: str):
    ext_mun = rec["municipio"]["nomeIBGE"]
    ext_uf = rec["municipio"]["uf"]["sigla"]

    cod = str(rec["municipio"]["codigoIBGE"])
    uf = str(ext_uf).lower()
    mun = str(normalizar_municipio(ext_mun))

    name_file_output_json = f"{yyyymm[0:4]}/{yyyymm[4:6]}/-{uf}-{mun}-{cod}.json"
    return name_file_output_json

#Contador de requisição
def contador_requisicao():
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    if REQUEST_COUNT % REQUEST_LIMIT == 0:
        print(f"A consulta atingiu {REQUEST_COUNT} requisições. Pausando {PAUSE_SECONDS}s...")
        time.sleep(PAUSE_SECONDS)

#Acessa a API do Portal da Transparencia e extrai os Dados em formato JSON
def extracao_dados_api(URL_API_PORTAL_DA_TRANSPARENCIA, HEADERS_API_PORTAL_DA_TRANSPARENCIA, codigo, yyyymm, max_retries=3):

    url = f"{URL_API_PORTAL_DA_TRANSPARENCIA}?mesAno={yyyymm}&codigoIbge={codigo}&pagina=1"
    headers = HEADERS_API_PORTAL_DA_TRANSPARENCIA
    
    for attempt in range(max_retries):
        cont = contador_requisicao()
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception as e:
                raise RuntimeError(f"Falha ao decodificar JSON: {e}")
            except requests.exceptions.SSLError as e:
                print(f"Erro SSL na tentativa {attempt}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão/tentativa {attempt}: {e}")
        elif resp.status_code in (429, 500, 502, 503, 504):
            time.sleep(20)  
            #continue
        else:
            raise RuntimeError(f" {cont} Erro {resp.status_code} -> {resp.text[:200]}")
    raise RuntimeError(f"Falha após {max_retries} tentativas: {url}")

#Faz o input no MINIO na camada BRONZE
def put_json_minio(s3_client, bucket: str, key: str, obj: dict):
    body = io.BytesIO(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")

#Inclusão de dados na camada Bronze 
total_enviados = 0
for yyyymm in datas(DATA_INICIO, DATA_FIM) :
    for codigo in codigos_ibge(URL_API_IBGE):
        registros = extracao_dados_api(URL_API_PORTAL_DA_TRANSPARENCIA, HEADERS_API_PORTAL_DA_TRANSPARENCIA, codigo, yyyymm, max_retries=3)
        if not registros:
            break
        for rec in registros:
            name_file_output_json = nome_arquivo_output(rec, yyyymm)
            put_json_minio(s3_client, BUCKET, name_file_output_json, rec)
            total_enviados += 1

        #print(f"[OK] {codigo} {yyyymm}: enviados {total_enviados} até agora")