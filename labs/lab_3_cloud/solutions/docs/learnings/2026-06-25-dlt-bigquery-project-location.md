---
date: 2026-06-25
topic: dlt BigQuery Project and Location Config
---

# dlt Pipeline: Explicit BigQuery Project and Location

## The Problem / Context
When running the dlt pipeline with `PIPELINE_DESTINATION=bigquery`, dlt used Application Default Credentials (ADC) which resolved to a different GCP project than intended. The `GCP_PROJECT_ID` env var was only used in application logging — dlt ignored it. This caused data to land in the wrong project, and subsequent dbt builds failed with "dataset not found".

Additionally, BigQuery requires the query job location to match the dataset location exactly. If the Terraform-provisioned dataset is in `us-central1` but dlt defaults to `US` (multi-region), the load fails.

## The Solution / Learning
Set dlt's BigQuery config explicitly via environment variables before creating the pipeline:

```python
os.environ.setdefault("DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID", gcp_project_id)
os.environ.setdefault("DESTINATION__BIGQUERY__LOCATION", gcp_location)
os.environ.setdefault("DESTINATION__FILESYSTEM__BUCKET_URL", bucket_url)
```

**Key insight:** dlt does NOT read `GCP_PROJECT_ID` or `GCP_LOCATION` — it uses its own config namespace (`DESTINATION__BIGQUERY__*`). Always set these explicitly when the ADC default project differs from your target project.

Also: after a failed dlt load, the pipeline state can become stale. Delete `~/.dlt/pipelines/<name>` to reset completely before retrying.
