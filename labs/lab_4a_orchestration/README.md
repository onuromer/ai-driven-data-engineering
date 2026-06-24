# Lab 4a — Orchestrate It: Pipeline Scheduling with Airflow

*Optional lab — for faster groups, extended workshops, or take-home exercise.*

In this lab you'll have AI create an Apache Airflow DAG that orchestrates the full data pipeline (dlt ingestion → dbt transformation) on a schedule.

## Learning Objectives

- Use the full AI workflow cycle (PRD → tasks → implement → finalize) for a new feature
- See how AI handles orchestration code (Airflow DAGs, task dependencies)
- Connect the ingestion and transformation layers into an automated pipeline

## Tools

| | |
|---|---|
| **Tool type** | CLI or IDE (your choice) |
| **Environment** | GCP (Cloud Composer) or Local (standalone Airflow) |
| **Duration** | 60–75 minutes |

## Prerequisites

- Labs 0–3 completed (working pipeline on GCP)
- Airflow environment available (Cloud Composer instance or local Airflow)

## Steps

### Step 1 — Create a PRD for Orchestration (10 min)

1. Copy the prompt from [`prompts/01_create_prd.md`](prompts/01_create_prd.md) into your AI assistant
2. Answer clarifying questions based on the prompt guidance
3. Review the generated PRD — it should cover the DAG structure, schedule, and dependencies

### Step 2 — Create Tasks and Implement (40–50 min)

1. Use `create-tasks` to generate task breakdowns
2. Create a feature branch with `git-worktree`
3. Use `implement-tasks` with the prompt from [`prompts/02_implement_orchestration.md`](prompts/02_implement_orchestration.md)
4. The AI should create an Airflow DAG that:
   - Runs the dlt ingestion pipeline
   - Triggers `dbt build` after ingestion completes
   - Handles errors and retries
   - Runs on a configurable schedule (daily by default)

### Step 3 — Test and Finalize (10–15 min)

1. Deploy the DAG to your Airflow environment
2. Trigger a manual run and verify it completes
3. Use `finalize-tasks` to create a PR

## Checkpoints

- [ ] PRD for orchestration feature exists
- [ ] Airflow DAG file created (e.g., `dags/pokedex_pipeline.py`)
- [ ] DAG has tasks for ingestion and transformation in correct order
- [ ] DAG runs successfully (manual trigger)
- [ ] PR created

## Next

Try another optional lab:
- [Lab 4b — Visualize It](../lab_4b_visualization/README.md)
- [Lab 4c — AI/ML on It](../lab_4c_ai_ml/README.md)
