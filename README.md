# PySpark Databricks CI/CD Sample

This repository is a complete starter template for:
- building a PySpark project
- testing it in GitHub Actions
- deploying and running it in Databricks using Databricks Asset Bundles

## Project layout

- `src/main.py`: pipeline entrypoint and reusable run logic
- `src/utils.py`: PySpark transformation logic
- `jobs/main.py`: Databricks job entrypoint
- `tests/`: unit tests executed in CI
- `databricks.yml`: Databricks bundle definition
- `resources/sample_job.yml`: Databricks job resource
- `.github/workflows/ci.yml`: CI workflow (tests)
- `.github/workflows/deploy-databricks.yml`: CD workflow (validate, deploy, run)

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m src.main --output-path /tmp/pyspark_databricks_cicd/local_run
```

## Databricks prerequisites

1. Create a Databricks personal access token (PAT).
2. Identify an existing cluster ID where the job can run.
3. Add these GitHub repository secrets:
   - `DATABRICKS_HOST` (example: `https://adb-1234567890123456.7.azuredatabricks.net`)
   - `DATABRICKS_TOKEN`
   - `DATABRICKS_CLUSTER_ID`

## CI/CD flow

### CI (`.github/workflows/ci.yml`)
- Runs on pull requests and non-main pushes.
- Installs Python + Java + dependencies.
- Runs `pytest`.

### CD (`.github/workflows/deploy-databricks.yml`)
- Runs on pushes to `main` and manual trigger.
- Uses Databricks CLI in bundle mode.
- Executes:
  - `databricks bundle validate`
  - `databricks bundle deploy`
  - `databricks bundle run sample_pyspark_job`

## Manual deploy (optional)

```bash
export DATABRICKS_HOST="https://<your-databricks-workspace>"
export DATABRICKS_TOKEN="<your-token>"
databricks bundle validate -t dev --var="cluster_id=<your-cluster-id>"
databricks bundle deploy -t dev --var="cluster_id=<your-cluster-id>"
databricks bundle run sample_pyspark_job -t dev --var="cluster_id=<your-cluster-id>"
```
