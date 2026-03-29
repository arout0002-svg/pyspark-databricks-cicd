# Databricks notebook source
# MAGIC %md
# MAGIC # Sample PySpark Notebook
# MAGIC
# MAGIC This notebook executes the same transformation logic used by the packaged job.

# COMMAND ----------

from src.main import run_pipeline

output_path = "/tmp/pyspark_databricks_cicd/notebook_output"
rows = run_pipeline(spark, output_path)
print(f"Notebook pipeline completed. Rows written: {rows}")