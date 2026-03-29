from pyspark.sql import SparkSession

from src.utils import transform_orders


def test_transform_orders_adds_expected_columns() -> None:
    spark = SparkSession.builder.master("local[1]").appName("test-utils").getOrCreate()

    source_df = spark.createDataFrame(
        [("john doe", 100.0, "books")],
        ["customer_name", "amount", "category"],
    )
    transformed_df = transform_orders(source_df)
    row = transformed_df.collect()[0]

    assert row["customer_name"] == "John Doe"
    assert row["amount_usd"] == 110.0
    assert row["is_large_order"] is True

    spark.stop()
