locals {
  data_lake_bucket = "data-lake"
}

variable "project_id" {
  description = "Your GCP Project ID"
  type = string
  default = "github-repos-data-exploration"
}

variable "region" {
  description = "Region for GCP resources"
  type = string
  default = "us"
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default = "STANDARD"
}

variable "bq_dataset" {
  description = "BigQuery Dataset"
  type = string
  default = "github_repos_data_exploration_dataset"
}

variable "output_variables_file_path" {
  description = "Path to the file to store output variables for reference"
  type = string
  default = "../vars.conf"
}
