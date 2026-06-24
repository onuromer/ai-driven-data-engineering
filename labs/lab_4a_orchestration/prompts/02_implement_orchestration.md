# Prompt: Implement Orchestration with Managed Service for Apache Airflow

Copy the prompt below into your AI coding assistant.

~~~
Use skill: implement-tasks

Read the orchestration tasks in docs/tasks/ and implement the full end-to-end pipeline orchestration with Managed Service for Apache Airflow deployment.

1. AIRFLOW DAG

Location: dags/pokedex_pipeline.py
DAG ID: pokedex_data_pipeline
Schedule: @daily (configurable via Airflow Variable)

Tasks in order:
1. run_ingestion — Execute the dlt pipeline (ingestion/pipeline.py) targeting BigQuery
2. dbt_deps — Run dbt deps to install packages
3. dbt_build — Run dbt build --target prod in the transform/ directory
4. dbt_docs — Run dbt docs generate

Dependencies: run_ingestion >> dbt_deps >> dbt_build >> dbt_docs

Implementation notes:
- Use BashOperator for all tasks (simple, portable)
- Add retries=3 and retry_delay=timedelta(minutes=5) as defaults
- Set catchup=False
- Use Airflow Variables for configurable parameters (project_id, dataset names, pipeline destination)
- Add DAG documentation (doc_md) explaining what the pipeline does
- No hardcoded credentials — use Airflow Variables and environment

2. TERRAFORM FOR CLOUD COMPOSER

Extend the existing infra/ directory with Managed Service for Apache Airflow resources:

infra/
├── ... (existing BigQuery, GCS files)
├── composer.tf          # Managed Service for Apache Airflow environment
├── composer_iam.tf      # Service account and IAM for the Airflow environment
└── composer_network.tf  # VPC network for the Airflow environment (if needed)

Requirements:
- Managed Service for Apache Airflow with image_version "composer-2-airflow-2"
- ENVIRONMENT_SIZE_SMALL
- pypi_packages: dbt-core, dbt-bigquery, dlt[bigquery], requests
- Upload DAG files from dags/ to the Airflow GCS bucket using google_storage_bucket_object
- Create a variables.json with project config and upload to Airflow GCS data/ folder
- Import variables via a local-exec provisioner: gcloud composer environments run ... variables import

3. TESTING

- Create a test that validates the DAG can be parsed by Airflow without errors
- Verify task dependencies are in the correct order
- Test that variables.json contains all required keys
~~~

## While the AI Works

Observe how it handles:
- Structuring the Terraform for the Airflow environment (VPC, service accounts, IAM)
- Configuring `pypi_packages` for the Airflow environment
- DAG deployment via GCS bucket objects
- Airflow Variable management
