# Prompt: Create PRD for Pipeline Orchestration

Copy the prompt below into your AI coding assistant.

~~~
Act as a Senior Data Engineer. Create a Product Requirements Document (PRD) for pipeline orchestration.

Use skill: create-prd

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

Managed Service for Apache Airflow Infrastructure (Terraform):
- Provision a Managed Service for Apache Airflow 2 environment using Terraform (extend existing infra/ directory)
- Use ENVIRONMENT_SIZE_SMALL for the workshop
- Include pypi_packages for dbt-core, dbt-bigquery, dlt[bigquery], and any other dependencies
- Deploy DAG files to the Airflow GCS bucket via Terraform
- Configure Airflow Variables via a variables.json uploaded to GCS

DAG Deployment:
- DAG files in dags/ directory
- Terraform uploads DAGs to the Airflow environment's GCS dags/ folder
- Airflow Variables stored in a variables.json (project_id, dataset names, pipeline config)
- Variables imported via gcloud composer environments run ... variables import

TECHNICAL CONSTRAINTS

- Use Airflow 2.x with Managed Service for Apache Airflow (composer-2-airflow-2 image)
- For dbt execution: prefer Cosmos (astronomer-cosmos) if available, which creates per-model Airflow tasks with individual retries and visibility. Fall back to BashOperator (dbt build) for simplicity if Cosmos adds too much complexity.
- Include astronomer-cosmos in pypi_packages if using Cosmos
- No hardcoded paths, project IDs, or credentials — use Airflow Variables and Connections
- The Airflow service account needs BigQuery Editor and GCS permissions

~~~
