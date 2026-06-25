# Prompt: Implement Orchestration with Managed Airflow

Copy the prompt below into your AI coding assistant.

~~~
Use skill: implement-tasks

Read the orchestration tasks in docs/tasks/ and implement the full end-to-end pipeline orchestration with Managed Airflow deployment.

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

2. TERRAFORM FOR MANAGED AIRFLOW (COMPOSER 3)

Important: Use Composer 3 (NOT Composer 2). This requires the google-beta provider.

Extend the existing infra/ directory:

infra/
├── ... (existing BigQuery, GCS files)
├── composer.tf          # Composer 3 environment + DAG/dbt deployment + variables

Composer 3 setup:
- Use google-beta provider
- Enable composer.googleapis.com API
- Create a custom service account (google_service_account) with roles/composer.worker
- Create the Composer environment (google_composer_environment) with:
  - provider = google-beta
  - image_version = "composer-3-airflow-2.11.1-build.6" (or similar composer-3 version)
  - node_config.service_account = the custom service account
  - No VPC or subnet needed (Composer 3 manages networking internally)
  - pypi_packages: dbt-core, dbt-bigquery, dlt[bigquery], requests, google-cloud-storage
- depends_on: API enablement and service account creation

File deployment:
- Upload DAG files from dags/ to the Composer GCS bucket using google_storage_bucket_object
- Upload dbt project files to dags/transform/ subdirectory
- Upload ingestion scripts to dags/ingestion/ subdirectory
- Create and upload variables.json to the GCS data/ folder
- Import variables via gcloud composer environments run ... variables import (local-exec provisioner)

Outputs:
- composer_environment_name
- composer_airflow_uri (Airflow UI URL)
- composer_gcs_bucket

3. TESTING

- Create a test that validates the DAG can be parsed by Airflow without errors
- Verify task dependencies are in the correct order
- Test that variables.json contains all required keys
~~~

## While the AI Works

Observe how it handles:
- Setting up Composer 3 with the google-beta provider
- Creating the service account and IAM bindings
- DAG and dbt file deployment to the GCS bucket
- Airflow Variable management
