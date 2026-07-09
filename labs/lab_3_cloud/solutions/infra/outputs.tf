output "bigquery_dataset_raw" {
  description = "BigQuery dataset ID for the raw data layer."
  value       = google_bigquery_dataset.pokedex_raw.dataset_id
}

output "bigquery_dataset_staging" {
  description = "BigQuery dataset ID for the staging data layer."
  value       = google_bigquery_dataset.pokedex_staging.dataset_id
}

output "bigquery_dataset_marts" {
  description = "BigQuery dataset ID for the marts data layer."
  value       = google_bigquery_dataset.pokedex_marts.dataset_id
}

output "gcs_staging_bucket_name" {
  description = "Name of the GCS bucket for dlt staging files."
  value       = google_storage_bucket.dlt_staging.name
}

output "gcs_staging_bucket_url" {
  description = "URL of the GCS bucket for dlt staging files."
  value       = google_storage_bucket.dlt_staging.url
}
