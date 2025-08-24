from config_spark import get_spark
from pyspark.sql.functions import col, trim, upper, lit, current_timestamp, xxhash64


SILVER_BUCKET = "s3a://silver-bolsa-familia-parquet/"
GOLD_BUCKET   = "s3a://gold-bolsa-familia-parquet/dim_uf"

spark = get_spark("dim_uf_gold-from-silver")


df = spark.read.parquet(SILVER_BUCKET)


dim = (df.select(
        upper(trim(col("uf"))).alias("uf_sigla"),
        trim(col("uf_nome")).alias("uf_nome"),
        col("cod_reg").alias("cod_regiao")
    )
    .dropna(subset=["uf_sigla"])
    .dropDuplicates(["uf_sigla"])
    .withColumn("uf_sk", xxhash64(col("uf_sigla")))
    .withColumn("ativo", lit(True))
    .withColumn("dt_criacao", current_timestamp())
    .select("uf_sk","uf_sigla","uf_nome","cod_regiao","ativo","dt_criacao")
)

(dim.write
    .mode("overwrite")
    .parquet(GOLD_BUCKET))