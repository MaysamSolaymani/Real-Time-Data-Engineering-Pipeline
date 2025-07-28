from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, TimestampType

if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .getOrCreate()

    schema = StructType() \
        .add("user_id", StringType()) \
        .add("action", StringType()) \
        .add("timestamp", StringType())

    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .option("startingOffsets", "earliest") \
        .load()

    df_parsed = df.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")

    clicks = df_parsed.filter(col("action") == "click")

    query = clicks.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
