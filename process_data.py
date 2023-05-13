import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month, dayofmonth, col


parser = argparse.ArgumentParser()

parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

spark = SparkSession.builder.appName('test').getOrCreate()

df_repos = spark.read.parquet(args.input)

df_repos= df_repos.withColumn("year", year(col("last_updated")))
df_repos= df_repos.withColumn("month", month(col("last_updated")))
df_repos= df_repos.withColumn("date", dayofmonth(col("last_updated")))
df_repos = df_repos.drop("last_updated")

df_repos.write.option("header",True).partitionBy("year", "month", "date") \
    .parquet(args.output, mode="overwrite")
