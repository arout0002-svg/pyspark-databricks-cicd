from pathlib import Path

from pyspark.sql import SparkSession

from src.main import run_pipeline


def test_run_pipeline_writes_rows(tmp_path: Path) -> None:
    spark = SparkSession.builder.master("local[1]").appName("test-main").getOrCreate()
    output_path = str(tmp_path / "orders_output")

    row_count = run_pipeline(spark, output_path)
    result_df = spark.read.parquet(output_path)

    assert row_count == 3
    assert result_df.count() == 3

    spark.stop()


def test_run_pipeline_without_output_path() -> None:
    spark = SparkSession.builder.master("local[1]").appName("test-main-no-write").getOrCreate()

    row_count = run_pipeline(spark)

    assert row_count == 3

    spark.stop()