# Lab 3 — Ship It: Go to Cloud

Requirements change — just like in the real world. In this lab, the project needs to move from local DuckDB to **Google BigQuery on GCP**. You'll update the PRD with new cloud requirements, generate new tasks, then have AI produce Terraform files and adapt the pipeline.

This lab demonstrates two things: AI handles Infrastructure-as-Code just as well as application code, and your context engineering workflow scales to evolving requirements.

## Learning Objectives

- Update an existing PRD when requirements change (re-planning with AI)
- Use AI to generate Terraform (HCL) for GCP infrastructure
- Adapt an existing dlt + dbt pipeline from DuckDB to BigQuery
- Experience the full cycle: update PRD → create tasks → implement → finalize

## Tools

| | |
|---|---|
| **Tool type** | Your choice — CLI or IDE (you've used both, pick what works for you) |
| **Environment** | Local + GCP Playground |
| **Duration** | 60–75 minutes |

## Prerequisites

- Labs 0–2 completed (working local pipeline with dlt + dbt)
- GCP Playground project access provided by the instructor
- Terraform installed (1.0+)
- `gcloud` CLI authenticated to the playground project

## Steps

### Step 1 — Update the PRD (10 min)

Requirements have changed. Use the prompt from [`prompts/01_update_prd.md`](prompts/01_update_prd.md) to update the existing PRD with cloud requirements.

1. Copy the prompt into your AI assistant
2. The AI will read the existing PRD and add cloud-specific requirements
3. Review the updated PRD — does it now cover Terraform, BigQuery, and GCS?

### Step 2 — Create New Tasks (10 min)

Use the prompt from [`prompts/02_create_tasks.md`](prompts/02_create_tasks.md) to generate tasks for the cloud migration.

1. Copy the prompt into your AI assistant
2. Review the generated tasks — they should cover infrastructure, pipeline adaptation, and testing
3. Type **"Go"** to generate detailed sub-tasks

### Step 3 — Implement Terraform Infrastructure (20 min)

Use the prompt from [`prompts/03_implement_cloud.md`](prompts/03_implement_cloud.md) to have AI create Terraform files and adapt the pipeline.

1. Copy the prompt into your AI assistant
2. The AI will create Terraform configurations in `infra/`
3. Review the generated Terraform before applying:
   - BigQuery dataset(s)
   - GCS bucket for dlt staging
   - IAM / service account if needed
4. Apply the Terraform:
   ```bash
   cd infra
   terraform init
   terraform plan
   terraform apply
   ```

### Step 4 — Adapt the Pipeline (15 min)

Continue with the AI to adapt the dlt and dbt configurations:

1. **dlt:** Update the pipeline destination from DuckDB to BigQuery
   - Add BigQuery credentials configuration
   - Adjust the pipeline script to support both destinations (env variable)
2. **dbt:** Update the dbt profile to target BigQuery
   - Add `dbt-bigquery` adapter configuration in `profiles.yml`
   - Verify models are compatible with BigQuery SQL dialect

### Step 5 — Run End-to-End on GCP (10 min)

1. Run the dlt pipeline targeting BigQuery:
   ```bash
   uv run python ingestion/pipeline.py
   ```
2. Run dbt against BigQuery:
   ```bash
   cd transform
   dbt build --target prod
   ```
3. Verify data in BigQuery — ask the AI to help you query it
4. Run the tests to validate everything works

### Step 6 — Document Learnings (5 min)

Capture what you learned during this lab.

1. Tell your AI assistant what you learned or what surprised you:
   ```
   Use skill: document-learnings
   ```
2. The AI will create a file in `docs/learnings/` with the key takeaway

### Step 7 — Finalize (5 min)

1. Use `finalize-tasks` to clean up and create a PR
2. Review the PR — it should include Terraform files, pipeline changes, and updated dbt config

## Checkpoints

- [ ] PRD updated with cloud migration requirements
- [ ] New task file generated for cloud work
- [ ] Terraform files exist in `infra/` directory
- [ ] Terraform applied successfully to GCP Playground
- [ ] BigQuery dataset created
- [ ] GCS bucket created (for dlt staging)
- [ ] dlt pipeline runs and loads data into BigQuery
- [ ] dbt models run against BigQuery (`dbt build --target prod`)
- [ ] Pipeline supports both DuckDB (dev) and BigQuery (prod) destinations
- [ ] PR created via `finalize-tasks`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Terraform auth fails | Run `gcloud auth application-default login` and set your project: `gcloud config set project <PROJECT_ID>` |
| Terraform plan shows errors | Check that the GCP APIs are enabled (BigQuery, Cloud Storage). Ask the instructor if the playground is set up correctly |
| dlt can't connect to BigQuery | Verify credentials — `dlt` can use Application Default Credentials. Check `gcloud auth application-default print-access-token` works |
| dbt BigQuery dialect errors | Some DuckDB SQL syntax differs from BigQuery (e.g., `::` casting). Ask the AI to fix dialect-specific issues |
| Permission denied on GCP | Ask the instructor to verify your playground access — you need BigQuery Editor and Storage Admin roles |

## Next

You've completed the core workshop! If time allows, continue with one of the optional labs:
- [Lab 4a — Orchestrate It](../lab_4a_orchestration/README.md) — Schedule the pipeline with Airflow
- [Lab 4b — Visualize It](../lab_4b_visualization/README.md) — Build a Streamlit dashboard
- [Lab 4c — AI/ML on It](../lab_4c_ai_ml/README.md) — Train BQML models and use Gemini on your data
