#!/usr/bin/env bash
set -euo pipefail

# Lab 4b — Prepare: Copy Lab 0-3 solutions and ensure DuckDB has data
# Usage: bash labs/lab_4b_visualization/prepare.sh ~/my-pokedex-project

PROJECT_DIR="${1:?Usage: $0 <project-dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Run Lab 3 prepare first (includes Labs 0-2)
bash "$REPO_DIR/labs/lab_3_cloud/prepare.sh" "$PROJECT_DIR"

echo ""
echo "==> Preparing Lab 4b: Copying Lab 3 solutions to $PROJECT_DIR"

# Lab 3: Terraform + adapted pipeline + dbt config + learnings + .env.example
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/infra" "$PROJECT_DIR/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/ingestion/pipeline.py" "$PROJECT_DIR/ingestion/"
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/transform/" "$PROJECT_DIR/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/prds/"* "$PROJECT_DIR/docs/prds/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/tasks/"* "$PROJECT_DIR/docs/tasks/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/.env.example" "$PROJECT_DIR/"
if [ -d "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings" ]; then
    cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings/"* "$PROJECT_DIR/docs/learnings/"
fi
echo "    Lab 3 solutions copied (Terraform + pipeline + dbt + .env.example + learnings)"

echo ""
echo "==> Ready for Lab 4b!"
echo "    Follow the instructions in labs/lab_4b_visualization/README.md"
