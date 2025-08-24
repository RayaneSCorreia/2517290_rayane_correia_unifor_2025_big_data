from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month
import pyspark
from config_spark import get_spark

BRONZE_BUCKET = "s3a://bronze-bolsa-familia-json/"
SILVER_BUCKET = "s3a://silver-bolsa-familia-parquet/"

df = (spark.read
      .option("recursiveFileLookup", "true")
      .option("pathGlobFilter", "*.json")
      .option("multiLine", "true") 
      .json(BRONZE_BUCKET))

df_final = (
    df.select(
        col("id"),
        col("dataReferencia").alias("dt_ref"),
        col("municipio.codigoIBGE").alias("cod_mun"),
        col("municipio.nomeIBGE").alias("mun_nome"),
        col("municipio.codigoRegiao").alias("cod_reg"),
        col("municipio.uf.sigla").alias("uf"),
        col("municipio.uf.nome").alias("uf_nome"),
        col("tipo.id").alias("id_tp"),
        col("tipo.descricao").alias("tp_desc"),
        col("tipo.descricaoDetalhada").alias("tp_desc_det"),
        col("quantidadeBeneficiados").alias("quantidade_beneficiados"),
        col("valor").cast("double").alias("valor")
        )
    ).withColumn("dt_ref", to_date(col("dt_ref"), "yyyy-MM-dd")).withColumn("ano", year(col("dt_ref"))).withColumn("mes", month(col("dt_ref")))

(df_final.repartition("uf","ano","mes")
       .write
       .mode("overwrite")
       .option("partitionOverwriteMode","dynamic")
       .partitionBy("uf","ano","mes")
       .parquet(SILVER_BUCKET))