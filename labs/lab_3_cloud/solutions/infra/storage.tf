# GCS bucket for dlt pipeline staging files.
# dlt uses this bucket for intermediate file staging during BigQuery loads.

resource "google_storage_bucket" "dlt_staging" {
  name     = var.gcs_bucket_name
  project  = var.gcp_project_id
  location = var.gcp_location

  uniform_bucket_level_access = true
  force_destroy               = true

  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    environment = "prod"
    purpose     = "dlt-staging"
    managed_by  = "terraform"
  }
}
