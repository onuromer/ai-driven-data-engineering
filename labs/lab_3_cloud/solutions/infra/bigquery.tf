# BigQuery datasets for the medallion architecture layers.
# Each dataset mirrors a schema in the local DuckDB database.

resource "google_bigquery_dataset" "pokedex_raw" {
  dataset_id  = "pokedex_raw"
  description = "Raw data layer — unmodified data as extracted from PokeAPI by dlt."
  project     = var.gcp_project_id
  location    = var.gcp_location

  delete_contents_on_destroy = true

  labels = {
    environment = "prod"
    layer       = "raw"
    managed_by  = "terraform"
  }
}

resource "google_bigquery_dataset" "pokedex_staging" {
  dataset_id  = "pokedex_staging"
  description = "Staging data layer — cleaned, typed, 1:1 mappings of raw tables."
  project     = var.gcp_project_id
  location    = var.gcp_location

  delete_contents_on_destroy = true

  labels = {
    environment = "prod"
    layer       = "staging"
    managed_by  = "terraform"
  }
}

resource "google_bigquery_dataset" "pokedex_marts" {
  dataset_id  = "pokedex_marts"
  description = "Marts data layer — analytical models with joins, aggregations, and business logic."
  project     = var.gcp_project_id
  location    = var.gcp_location

  delete_contents_on_destroy = true

  labels = {
    environment = "prod"
    layer       = "marts"
    managed_by  = "terraform"
  }
}
