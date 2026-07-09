#!/usr/bin/env bash
set -euo pipefail

# Lab 2 — Prepare: Copy Lab 0 + Lab 1 solutions and ensure DuckDB has data
# Usage: bash labs/lab_2_transformation/prepare.sh ~/my-pokedex-project

PROJECT_DIR="${1:?Usage: $0 <project-dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "==> Preparing Lab 2: Copying Lab 0 + Lab 1 solutions to $PROJECT_DIR"

# Lab 0: PRD + tasks
mkdir -p "$PROJECT_DIR/docs/prds" "$PROJECT_DIR/docs/tasks" "$PROJECT_DIR/docs/learnings"
cp "$REPO_DIR/labs/lab_0_context_engineering/solutions/docs/prds/"* "$PROJECT_DIR/docs/prds/"
cp "$REPO_DIR/labs/lab_0_context_engineering/solutions/docs/tasks/"* "$PROJECT_DIR/docs/tasks/"
echo "    Lab 0 solutions copied (PRD + tasks)"

# Lab 1: Ingestion pipeline + tests + learnings
mkdir -p "$PROJECT_DIR/ingestion" "$PROJECT_DIR/tests"
cp "$REPO_DIR/labs/lab_1_ingestion/solutions/ingestion/"* "$PROJECT_DIR/ingestion/"
cp "$REPO_DIR/labs/lab_1_ingestion/solutions/tests/"* "$PROJECT_DIR/tests/"
cp "$REPO_DIR/labs/lab_1_ingestion/solutions/docs/learnings/"* "$PROJECT_DIR/docs/learnings/"
echo "    Lab 1 solutions copied (ingestion pipeline + tests + learnings)"

# Run pipeline if DuckDB doesn't exist
if [ ! -f "$PROJECT_DIR/data/pokedex.db" ]; then
    echo ""
    echo "==> DuckDB database not found. Running ingestion pipeline..."
    echo "    This will fetch data from PokeAPI (may take a few minutes)"
    cd "$PROJECT_DIR"
    uv run python ingestion/pipeline.py
    echo "    Pipeline complete!"
else
    echo "    DuckDB database already exists at data/pokedex.db"
fi

echo ""
echo "==> Ready for Lab 2!"
echo "    Follow the instructions in labs/lab_2_transformation/README.md"
