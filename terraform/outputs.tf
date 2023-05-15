output "project_id" {
  description = "Project ID"
  value       = var.project_id
}

output "data_lake_bucket_name" {
  description = "Bucket name"
  value       = google_storage_bucket.data_lake_bucket.name
}

output "bq_dataset" {
  description = "Big Query Dataset"
  value       = google_bigquery_dataset.bq_dataset.dataset_id
}

output "dataproc_cluster" {
  description = "Dataproc cluster name"
  value       = google_dataproc_cluster.dataproc_cluster.name
}
