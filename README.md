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

## Local test setup (recommended)

1. Create local env file:
   ```bash
   cp .env.local.example .env.local
   ```
2. Update `.env.local` with your Databricks values (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`).
3. Run local validation:
   ```bash
   chmod +x scripts/local_test.sh
   ./scripts/local_test.sh
   ```

This script runs `pytest` and, when Databricks CLI + env vars are available, also runs `databricks bundle validate -t dev`.

## Databricks prerequisites

1. Create a Databricks personal access token (PAT).
2. Add these GitHub repository secrets:
   - `DATABRICKS_HOST` (example: `https://adb-1234567890123456.7.azuredatabricks.net`)
   - `DATABRICKS_TOKEN`
   - Keep secret values plain (no leading/trailing spaces, no `KEY:` prefix)
3. This template uses Databricks serverless job environments (compatible with serverless-only workspaces).
4. `DATABRICKS_CLUSTER_ID=auto` is accepted in local envs for compatibility, but it is not used by the current serverless job configuration.

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
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run sample_pyspark_job -t dev
```

No cluster sizing variables are needed for the default serverless setup.
