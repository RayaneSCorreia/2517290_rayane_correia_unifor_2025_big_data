from pyspark.sql.functions import col, trim, upper, lit, current_timestamp, xxhash64
from config_spark import get_spark

SILVER_BUCKET = "s3a://silver-bolsa-familia-parquet/"
GOLD_BUCKET   = "s3a://gold-bolsa-familia-parquet/dim_municipio"

spark = get_spark("dim_municipio_from_silver")

df = spark.read.parquet(SILVER_BUCKET)

dim = (df
    .select(
        col("cod_mun").cast("string").alias("cod_mun_ibge"),
        trim(col("mun_nome")).alias("mun_nome"),
        upper(trim(col("uf"))).alias("uf_sigla"),
        trim(col("uf_nome")).alias("uf_nome"),
        col("cod_reg").alias("cod_regiao")
    )
    .dropna(subset=["cod_mun_ibge"])
    .dropDuplicates(["cod_mun_ibge"])
    .withColumn("mun_sk", xxhash64(col("cod_mun_ibge")))
    .withColumn("ativo", lit(True))
    .withColumn("dt_criacao", current_timestamp())
    .select("mun_sk","cod_mun_ibge","mun_nome","uf_sigla","uf_nome","cod_regiao","ativo","dt_criacao")
)

(dim.repartition("uf_sigla")
    .write
    .mode("overwrite")
    .partitionBy("uf_sigla")
    .parquet(GOLD_BUCKET))