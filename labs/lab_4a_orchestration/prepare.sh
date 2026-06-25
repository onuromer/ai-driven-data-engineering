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

# Lab 3: Terraform
cp -r "$REPO_DIR/labs/lab_3_cloud/solutions/infra" "$PROJECT_DIR/"

# Lab 3: Adapted pipeline
cp "$REPO_DIR/labs/lab_3_cloud/solutions/ingestion/pipeline.py" "$PROJECT_DIR/ingestion/"

# Lab 3: Adapted dbt (overwrite Lab 2's versions)
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/dbt_project.yml" "$PROJECT_DIR/transform/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/profiles.yml" "$PROJECT_DIR/transform/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/macros/"*.sql "$PROJECT_DIR/transform/macros/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/models/staging/"* "$PROJECT_DIR/transform/models/staging/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/models/marts/"* "$PROJECT_DIR/transform/models/marts/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/transform/tests/"*.sql "$PROJECT_DIR/transform/tests/"

# Lab 3: Updated PRD + tasks
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/prds/"* "$PROJECT_DIR/docs/prds/"
cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/tasks/"* "$PROJECT_DIR/docs/tasks/"

# Lab 3: .env.example
cp "$REPO_DIR/labs/lab_3_cloud/solutions/.env.example" "$PROJECT_DIR/"

# Lab 3: Learnings
if [ -d "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings" ]; then
    cp "$REPO_DIR/labs/lab_3_cloud/solutions/docs/learnings/"* "$PROJECT_DIR/docs/learnings/"
fi

echo "    Lab 3 solutions copied (Terraform + pipeline + dbt + .env.example + learnings)"

echo ""
echo "==> Ready for Lab 4a!"
echo "    Follow the instructions in labs/lab_4a_orchestration/README.md"
