# unifor-2025-av-bigdata
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
   ┣ 📂 f_bolsa_familia_hist/         # Scripts do pipeline Bolsa Família
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
- *Python (PySpark, Requests, Pandas)*  

---

## ▶ Como Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/projeto-bolsa-familia.git
cd projeto-bolsa-familia
