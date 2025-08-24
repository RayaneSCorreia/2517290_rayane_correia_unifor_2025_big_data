from config_spark import get_spark
from pyspark.sql.functions import col, year, month, sum as _sum, countDistinct

SILVER_BUCKET = "s3a://silver-bolsa-familia-parquet/"
GOLD_BUCKET   = "s3a://gold-bolsa-familia-parquet/f_bolsa_familia_mun_agg"

spark = get_spark("gold-from-silver-fato-bolsa-familia-agg")

df = spark.read.parquet(SILVER_BUCKET)

# cria agregação mensal por município
fact = (df
    .withColumn("ano", year(col("dt_ref")))
    .withColumn("mes", month(col("dt_ref")))
    .groupBy("ano", "mes", "cod_mun", "mun_nome", "uf", "uf_nome", "cod_reg")
    .agg(
        _sum("valor").alias("vl_total_mes"),
        _sum("quantidade_beneficiados").alias("qtd_beneficiados_mes"),
        countDistinct("id").alias("qtd_registros")
    )
    .orderBy("ano","mes","uf","mun_nome")
)

(fact.write
    .mode("overwrite")
    .partitionBy("ano","mes")
    .parquet(GOLD_BUCKET))