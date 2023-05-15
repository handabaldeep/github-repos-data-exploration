terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region
}

resource "google_service_account" "service_account" {
  account_id = "service-account"
  display_name = "Service account created via terraform"
}

resource "google_service_account_key" "service_account_key" {
  service_account_id = google_service_account.service_account.name
}

resource "local_file" "service_account_key" {
    content = base64decode(google_service_account_key.service_account_key.private_key)
    filename = "../service-account.json"
}

resource "google_project_iam_binding" "service_account_iam" {
  project = var.project_id
  for_each = toset([
    "roles/storage.admin",
    "roles/bigquery.admin"
  ])
  role = each.key
  members = [
    "serviceAccount:${google_service_account.service_account.email}"
  ]
}

resource "google_storage_bucket" "data_lake_bucket" {
  name = "${local.data_lake_bucket}-${var.project_id}"
  location = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true
  force_destroy = true
}

resource "google_bigquery_dataset" "bq_dataset" {
  dataset_id = var.bq_dataset
  location = var.region
}

resource "google_dataproc_cluster" "dataproc_cluster" {
  name = "${var.project_id}-cluster"
  region = "us-central1"

  cluster_config {

    master_config {
      num_instances = 1
      machine_type = "n2-standard-2"
    }

    worker_config {
      num_instances = 2
      machine_type = "n2-standard-2"
    }

    preemptible_worker_config {
      num_instances = 0
    }

    software_config {
      image_version = "2.0-debian10"
    }

  }
}
