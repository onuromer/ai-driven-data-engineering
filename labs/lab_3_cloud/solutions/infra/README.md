# Terraform Infrastructure

This directory contains Terraform configurations to provision GCP resources for the Pokedex data platform.

## Resources Created

| Resource | Name | Description |
|----------|------|-------------|
| BigQuery Dataset | `pokedex_raw` | Raw data layer — dlt pipeline output |
| BigQuery Dataset | `pokedex_staging` | Staging layer — cleaned dbt models |
| BigQuery Dataset | `pokedex_marts` | Marts layer — analytical dbt models |
| GCS Bucket | `<gcs_bucket_name>` | Staging bucket for dlt BigQuery loads |

## Prerequisites

1. **Google Cloud Project**: A GCP project must already exist.
2. **Google Cloud SDK**: Install [gcloud](https://cloud.google.com/sdk/docs/install) and authenticate:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Terraform**: Version >= 1.5. Install via [tfenv](https://github.com/tfutils/tfenv) or [direct download](https://www.terraform.io/downloads).
4. **Permissions**: Your account needs BigQuery Admin and Storage Admin roles on the project.

## Usage

```bash
cd infra

# 1. Create your variable values file
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your project-specific values

# 2. Initialize Terraform
terraform init

# 3. Preview changes
terraform plan

# 4. Apply changes
terraform apply

# 5. (Optional) Tear down resources
terraform destroy
```

## Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `gcp_project_id` | Yes | — | Google Cloud project ID |
| `gcp_location` | No | `us-central1` | GCP region for all resources |
| `gcs_bucket_name` | Yes | — | Name for the dlt staging GCS bucket |

## Outputs

After `terraform apply`, the following values are available:

| Output | Description |
|--------|-------------|
| `bigquery_dataset_raw` | Dataset ID for the raw layer |
| `bigquery_dataset_staging` | Dataset ID for the staging layer |
| `bigquery_dataset_marts` | Dataset ID for the marts layer |
| `gcs_staging_bucket_name` | GCS bucket name |
| `gcs_staging_bucket_url` | GCS bucket URL (`gs://...`) |
