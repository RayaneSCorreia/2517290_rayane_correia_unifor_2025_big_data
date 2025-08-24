# 2517290_rayane_correia_unifor_2025_big_data

Esse repositorio contém o trabalho final da disciplina Big Data e Tecnologias de Armazenamento ministrada pelo professoer Nauber Góis
# 📊 Pipeline de Dados – Bolsa Família

Este repositório contém a implementação de um *pipeline de dados completo* para ingestão, processamento e organização de dados do 
*Programa Bolsa Família*, utilizando **Spark, MinIO, Airflow e Docker**.
O projeto foi desenvolvido como parte da disciplina de Big Data – Pós UNIFOR.

---

## 🗂 Estrutura do Projeto

```bash
📂 Big Data/
 ┣ 📂 airflow/                      # Configurações e DAGs do Apache Airflow
   ┃ ┣ 📂 dags #Armazenamento de dags
     ┃ ┣ 📜 pipeline_bolsa_familia.py   # Orquestração principal do pipeline
 ┣ 📂 apps/                         # Scripts de aplicações (extração, transformação, carga)
   ┃ ┣ 📜 api-to-bronze.py # Extração da API → Bronze
   ┃ ┣ 📜 bronze-to-silver.py         # Transformação Bronze → Silver
   ┃ ┣ 📜 gold_dim_municipio_gold.py       # Dimensão Município
   ┃ ┣ 📜 gold_dim_uf_gold.py              # Dimensão UF
   ┃ ┣ 📜 gold_fact_bolsa_familia.py  # Fato Bolsa Família
   ┃ ┗ 📜 config_spark.py             # Configuração do Spark (integração com MinIO)
 ┣ 📂 data/                         # Armazenamento local simulado do Data Lake (MinIO)
   ┃ ┣ 📂 bronze-bolsa-familia-json   # Camada Bronze (dados brutos em JSON)
   ┃ ┣ 📂 silver-bolsa-familia-parquet # Camada Silver (dados tratados em Parquet)
   ┃ ┗ 📂 gold-bolsa-familia-parquet   # Camada Gold (modelos dimensionais e fatos)
 ┣ 📂 jars/                         # Dependências necessárias para Spark + MinIO
   ┃ ┣ link_para_extrair_aws-java-sdk-bundle-1.12.767.txt #o Git barrou pelo tamanho mas o txt tem o link para Download
   ┃ ┗ hadoop-aws-3.3.4.jar
 ┣ 📜 docker-compose.yml            # Orquestração dos serviços (Airflow, MinIO, Spark, Postgres)
 ┣ 📜 requirements.txt              # Dependências Python
```
## 🌐 APIs utilizadas & como obter a chave

### APIs utilizadas (links oficiais)
- *Portal da Transparência – Bolsa Família (por município)*  
  Utilizada para a camada Bronze (ingestão de parcelas por município).
- *IBGE – Localidades (Municípios/UF)*  
  Utilizada para referência de códigos IBGE e siglas de UF.

*Links úteis (documentação e catálogos)*
Portal da Transparência – Documentação geral:
https://portaldatransparencia.gov.br/api-de-dados

Portal da Transparência – Swagger (catálogo de endpoints):
https://api.portaldatransparencia.gov.br/

Portal da Transparência – Cadastro para obter a chave (token):
https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email

Conecta gov.br – Ficha do serviço (como acessar a API):
https://www.gov.br/conecta/catalogo/apis/portal-da-transparencia-do-governo-federal

IBGE – Documentação da API de Localidades:
https://servicodados.ibge.gov.br/api/docs/localidades 

## Como conseguir a chave (token) do Portal da Transparência — passo a passo
1) *Acesse* a página “API de dados – Cadastro” do Portal da Transparência e clique em *“Entrar com gov.br”*.  
2) *Autentique-se* com sua conta gov.br (selo *Prata/Ouro*) *ou* com *CPF + senha* (neste caso, *habilite a verificação em duas etapas*).  
3) *Confirme o cadastro:* a chave de acesso (token) é *enviada por e-mail* ao endereço vinculado ao seu gov.br.  
4) *Guarde o token:* ele será informado no cabeçalho das requisições quando você for usar a API em sistemas/relatórios.  
5) *Atenção aos limites:* existem limites por minuto; alguns endpoints (como *Bolsa Família por município*) ficam em uma cota mais restrita.  

> Observação prática: ao usar a API em qualquer ferramenta, inclua o token no cabeçalho conforme instruções oficiais do Portal (chave chave-api-dados).

---



## 🔄 Fluxo do Pipeline

1. *Extração (Bronze)*  
   - Conexão com a *API do Governo (Portal da Transparência)*.  
   - Armazenamento em formato *JSON* no bucket *bronze* do MinIO.  

2. *Transformação (Silver)*  
   - Processamento com *PySpark*.  
   - Limpeza, padronização e enriquecimento dos dados.  
   - Salvo em formato *Parquet* no bucket *silver*.  

3. *Modelagem (Gold)*  
   - Criação de *tabelas dimensionais* (dim_municipio, dim_uf).  
   - Construção da *tabela fato* (fato_bolsa_familia).  
   - Armazenamento em *Parquet* no bucket *gold*.  

4. *Orquestração*  
   - Todo o fluxo é *automatizado com Airflow*, que executa:
     - Extração da API.  
     - Transformação Bronze → Silver.  
     - Construção dos modelos Silver → Gold.  

---

## ⚙ Tecnologias Utilizadas

- *Apache Spark* (processamento distribuído)  
- *MinIO* (Data Lake – compatível com S3)  
- *Apache Airflow* (orquestração de pipelines)  
- *Postgres* (metadados do Airflow)  
- *Docker & Docker Compose* (containerização e orquestração local)  
- *Python (PySpark, Requests)*  

---

## ▶ Como executar localmente

1) *Subir os serviços*
 Dentro da pasta do arquivo executar:
```bash
docker-compose up -d
Esse comando vai inicar o conteiner e instanciar todos os serviços nas suas devidas portas:
Airflow (http://localhost:8088) e MinIO (http://localhost:9001) e Spark (http://localhost:8080)

Acesse: Airflow (http://localhost:8088) e MinIO (http://localhost:9001) e Spark (http://localhost:8080)
	2.	Executar a DAG
Na UI do Airflow, habilite e rode a DAG pipeline_bolsa_familia.
```
Saídas:


👩‍💻 Autora

Rayane Correia — Analytics Engineer | Pós-graduação em Engenharia de Dados – UNIFOR

