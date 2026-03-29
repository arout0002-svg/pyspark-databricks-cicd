from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def transform_orders(df: DataFrame) -> DataFrame:
    """Apply a simple business transformation to order data."""
    return (
        df.withColumn("amount_usd", F.round(F.col("amount") * F.lit(1.10), 2))
        .withColumn("customer_name", F.initcap(F.col("customer_name")))
        .withColumn("is_large_order", F.col("amount") >= F.lit(100.0))
    )