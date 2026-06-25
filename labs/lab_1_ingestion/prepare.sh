#!/usr/bin/env bash
set -euo pipefail

# Lab 1 — Prepare: Copy Lab 0 solutions to your project
# Usage: bash labs/lab_1_ingestion/prepare.sh ~/my-pokedex-project

PROJECT_DIR="${1:?Usage: $0 <project-dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "==> Preparing Lab 1: Copying Lab 0 solutions to $PROJECT_DIR"

# Lab 0: PRD + tasks
mkdir -p "$PROJECT_DIR/docs/prds" "$PROJECT_DIR/docs/tasks"
cp "$REPO_DIR/labs/lab_0_context_engineering/solutions/docs/prds/"* "$PROJECT_DIR/docs/prds/"
cp "$REPO_DIR/labs/lab_0_context_engineering/solutions/docs/tasks/"* "$PROJECT_DIR/docs/tasks/"

echo "    Lab 0 solutions copied (PRD + tasks)"
echo ""
echo "==> Ready for Lab 1!"
echo "    Follow the instructions in labs/lab_1_ingestion/README.md"
