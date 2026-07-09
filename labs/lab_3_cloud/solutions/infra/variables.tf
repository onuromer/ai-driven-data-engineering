variable "gcp_project_id" {
  description = "The Google Cloud project ID to deploy resources into."
  type        = string
}

variable "gcp_location" {
  description = "The GCP region/location for BigQuery datasets and GCS bucket."
  type        = string
  default     = "us-central1"
}

variable "gcs_bucket_name" {
  description = "Name of the GCS bucket for dlt pipeline staging files."
  type        = string
}
