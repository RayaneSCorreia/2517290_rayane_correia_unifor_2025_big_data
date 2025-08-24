from pyspark.sql import SparkSession

MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY     = "minioadmin"
SECRET_KEY     = "minioadmin"

HADOOP_AWS_JAR = "/opt/jars/hadoop-aws-3.3.4.jar"
AWS_SDK_JAR    = "/opt/jars/aws-java-sdk-bundle-1.12.767.jar"

def get_spark(app_name="my-app"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("spark://spark:7077")
        .config("spark.jars","/opt/jars/hadoop-aws-3.3.4.jar,/opt/jars/aws-java-sdk-bundle-1.12.767.jar")
        .config("spark.hadoop.fs.s3a.endpoint","http://minio:9000")
        .config("spark.hadoop.fs.s3a.path.style.access","true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled","false")
        .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", SECRET_KEY)
        .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem") 
        .getOrCreate())