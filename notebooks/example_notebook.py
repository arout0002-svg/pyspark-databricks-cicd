# Databricks notebook source
# MAGIC %md
# MAGIC # Sample PySpark Notebook
# MAGIC
# MAGIC This notebook executes the same transformation logic used by the packaged job.

# COMMAND ----------

from src.main import run_pipeline

rows = run_pipeline(spark)
print(f"Notebook pipeline completed. Rows processed: {rows}")