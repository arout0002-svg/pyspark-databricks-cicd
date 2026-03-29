from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("MyPySparkJob").getOrCreate()
    # Your PySpark job implementation here
    data = spark.read.csv("path/to/data.csv")
    data.show()
    
    spark.stop()


if __name__ == "__main__":
    main()