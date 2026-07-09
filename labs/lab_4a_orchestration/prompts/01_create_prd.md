# Prompt: Create PRD for Pipeline Orchestration

Copy the prompt below into your AI coding assistant.

~~~
Act as a Senior Data Engineer. Create a Product Requirements Document (PRD) for pipeline orchestration.

Use skill: create-prd

Important: The scope below is already well-defined. Only ask clarifying questions about areas that are genuinely ambiguous or missing. If everything is clear, proceed directly to generating the PRD.

FEATURE SCOPE

Add end-to-end pipeline orchestration using Apache Airflow on Managed Service for Apache Airflow (formerly Cloud Composer). The DAG should orchestrate the full data pipeline: dlt ingestion followed by dbt transformation, deployed and running in the cloud.

REQUIREMENTS

DAG Design:
- A single DAG that runs the full pipeline end-to-end
- Task 1: Run the dlt ingestion pipeline (ingestion/pipeline.py targeting BigQuery)
- Task 2: Run dbt deps to install dbt packages
- Task 3: Run dbt build --target prod (transformations + tests)
- Task 4: Run dbt docs generate for documentation
- Dependencies: ingestion >> dbt_deps >> dbt_build >> dbt_docs
- Schedule: Daily, configurable via Airflow Variables
- Error handling: Retry failed tasks up to 3 times with exponential backoff
- Set catchup=False to avoid backfilling

dbt Execution Strategy:
- Use BashOperator for all tasks (simple, portable, good for workshop scope)
- Do NOT use Cosmos (astronomer-cosmos) — it adds complexity beyond the workshop scope
- BashOperator commands: "dbt deps", "dbt build --target prod", "dbt docs generate"

GCP APIs (Terraform):
- Enable the Cloud Composer API (composer.googleapis.com) before creating the environment
- Use google_project_service with disable_on_destroy = false

Managed Service for Apache Airflow Infrastructure (Terraform):
- Use Composer 3 (NOT Composer 2) — it's simpler and doesn't require VPC/subnet setup
- Use the google-beta provider (required for Composer 3)
- Image version: use a composer-3-airflow-2 version (e.g., "composer-3-airflow-2.11.1-build.6")
- Create a custom service account with roles/composer.worker role
- Do NOT create a VPC or subnet — Composer 3 manages networking internally
- Include pypi_packages for dbt-core, dbt-bigquery, dlt[bigquery], requests, and google-cloud-storage
- Deploy DAG files to the Airflow GCS bucket via Terraform using google_storage_bucket_object
- Configure Airflow Variables via a variables.json uploaded to GCS data/ folder
- Import variables via gcloud composer environments run ... variables import (as a Terraform local-exec provisioner)

DAG Deployment:
- DAG files in dags/ directory
- The dbt project files (models, macros, profiles.yml) should be bundled alongside the DAG in the GCS bucket — do NOT clone from Git at runtime
- Terraform uploads both DAGs and dbt project files to the Airflow environment's GCS bucket

Airflow Variables (variables.json):
- gcp_project_id: The GCP project ID
- gcp_location: The BigQuery/GCS region
- gcs_bucket_name: The dlt staging bucket name
- pokemon_limit: Number of Pokemon to ingest (default: 151)
- pipeline_destination: Set to "bigquery"

Testing:
- Create a pytest test that validates the DAG file can be parsed without import errors
- Verify task dependencies are in the correct order
- No need for full end-to-end Airflow testing in the workshop — manual trigger and monitoring is sufficient

TECHNICAL CONSTRAINTS

- Use google-beta provider for Composer 3 support
- Use Airflow 2.x with Composer 3 image
- No hardcoded paths, project IDs, or credentials — use Airflow Variables
- The custom service account needs roles/composer.worker plus BigQuery Editor and GCS permissions

REFERENCE

See https://docs.cloud.google.com/composer/docs/composer-3/terraform-create-environments for Composer 3 Terraform setup.
~~~
