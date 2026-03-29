#!/usr/bin/env bash
set -euo pipefail

if [[ -f ".env.local" ]]; then
  set -a
  # shellcheck disable=SC1091
  source ".env.local"
  set +a
fi

echo "Running local unit tests..."
PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "${PYTHON_BIN}" ]]; then
  if [[ -x "./venv/bin/python" ]]; then
    PYTHON_BIN="./venv/bin/python"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    echo "Python not found. Install python3 or create ./venv first."
    exit 1
  fi
fi

"${PYTHON_BIN}" -m pip install -r requirements.txt >/dev/null
"${PYTHON_BIN}" -m pytest -q

if command -v databricks >/dev/null 2>&1; then
  if [[ -n "${DATABRICKS_HOST:-}" && -n "${DATABRICKS_TOKEN:-}" ]]; then
    echo "Running Databricks bundle validate..."
    if [[ -n "${SPARK_VERSION:-}" || -n "${NODE_TYPE_ID:-}" ]]; then
      databricks bundle validate -t dev \
        --var="spark_version=${SPARK_VERSION:-14.3.x-scala2.12}" \
        --var="node_type_id=${NODE_TYPE_ID:-Standard_DS3_v2}"
    else
      databricks bundle validate -t dev
    fi
  else
    echo "Skipping Databricks validate (DATABRICKS_HOST/TOKEN not set)."
  fi
else
  echo "Skipping Databricks validate (databricks CLI not installed)."
fi

if [[ -n "${DATABRICKS_CLUSTER_ID:-}" ]]; then
  echo "Note: DATABRICKS_CLUSTER_ID is ignored by current job-cluster config."
fi
