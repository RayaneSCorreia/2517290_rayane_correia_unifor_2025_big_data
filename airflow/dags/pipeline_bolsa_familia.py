from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "rayane",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="etl_bolsa_familia",
    default_args=default_args,
    description="Pipeline ETL Bolsa Família (Bronze -> Silver -> Gold)",
    schedule_interval="@daily",  # ou None se quiser disparar manual
    start_date=datetime(2025, 8, 1),
    catchup=False,
    tags=["bolsa_familia", "etl"],
) as dag:

    # 1. Extrai dados da API para Bronze
    bronze_task = BashOperator(
        task_id="extract_bronze",
        bash_command="python /opt/airflow/apps/extracao_dados_api_bronze.py"
    )

    # 2. Transforma JSON -> Silver (Parquet limpo)
    silver_task = BashOperator(
        task_id="transform_silver",
        bash_command="python /opt/airflow/apps/bronze-to-silver.py"
    )

    # 3. Cria dimensão de municípios (Gold)
    dim_municipio_task = BashOperator(
        task_id="dim_municipio_gold",
        bash_command="python /opt/airflow/apps/dim_municipio_gold.py"
    )

    # 4. Cria dimensão de UFs (Gold)
    dim_uf_task = BashOperator(
        task_id="dim_uf_gold",
        bash_command="python /opt/airflow/apps/dim_uf_gold.py"
    )

    # 5. Cria fato consolidado (Gold)
    fato_task = BashOperator(
        task_id="fato_gold",
        bash_command="python /opt/airflow/apps/fato_bolsa_familia_gold.py"
    )

    # Definir a ordem
    bronze_task >> silver_task >> [dim_municipio_task, dim_uf_task] >> fato_task