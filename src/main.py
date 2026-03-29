from __future__ import annotations

import argparse
from typing import Optional

from pyspark.sql import DataFrame, SparkSession

from src.utils import transform_orders


def create_sample_orders(spark: SparkSession) -> DataFrame:
    rows = [
        ("alice", 45.50, "books"),
        ("bob", 125.00, "electronics"),
        ("charlie", 210.75, "furniture"),
    ]
    return spark.createDataFrame(rows, ["customer_name", "amount", "category"])


def run_pipeline(spark: SparkSession, output_path: Optional[str] = None) -> int:
    source_df = create_sample_orders(spark)
    transformed_df = transform_orders(source_df)
    if output_path:
        transformed_df.write.mode("overwrite").parquet(output_path)
    return transformed_df.count()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run sample PySpark pipeline.")
    parser.add_argument(
        "--output-path",
        default="",
        help="Optional output path for transformed parquet data.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.appName("sample-pyspark-databricks-cicd").getOrCreate()
    row_count = run_pipeline(spark, args.output_path)
    print(f"Pipeline completed successfully. Rows processed: {row_count}")
    spark.stop()


if __name__ == "__main__":
    main()