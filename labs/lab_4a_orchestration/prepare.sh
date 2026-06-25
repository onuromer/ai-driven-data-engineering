#!/usr/bin/env bash
set -euo pipefail

# Lab 4a — Prepare: Copy Lab 0-3 solutions and ensure DuckDB has data
# Usage: bash labs/lab_4a_orchestration/prepare.sh ~/my-pokedex-project

PROJECT_DIR="${1:?Usage: $0 <project-dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Run Lab 3 prepare first (includes Labs 0-2)
bash "$REPO_DIR/labs/lab_3_cloud/prepare.sh" "$PROJECT_DIR"

echo ""
echo "==> Preparing Lab 4a: Copying Lab 3 solutions to $PROJECT_DIR"

# Lab 3: Terraform + adapted pipeline + dbt profiles + learnings
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/infra" "$PROJECT_DIR/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/ingestion/pipeline.py" "$PROJECT_DIR/ingestion/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/profiles.yml" "$PROJECT_DIR/transform/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/macros/generate_schema_name.sql" "$PROJECT_DIR/transform/macros/"
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/transform/models/staging/" "$PROJECT_DIR/transform/models/staging/"
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/transform/models/marts/" "$PROJECT_DIR/transform/models/marts/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/prds/"* "$PROJECT_DIR/docs/prds/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/tasks/"* "$PROJECT_DIR/docs/tasks/"
if [ -d "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings" ]; then
    cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings/"* "$PROJECT_DIR/docs/learnings/"
fi
echo "    Lab 3 solutions copied (Terraform + adapted pipeline + dbt BigQuery config + learnings)"

echo ""
echo "==> Ready for Lab 4a!"
echo "    Follow the instructions in labs/lab_4a_orchestration/README.md"
