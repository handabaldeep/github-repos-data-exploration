# Github Repos Data Exploration

Analysing the Open Source GitHub repositories using Data Engineering Tools

## Steps

0. Install all the required tools - `terraform`, `gcloud`, `poetry`
1. Create a project on GCP - `Github Repos Data Exploration`
2. Authenticate with GCP using gcloud CLI - `gcloud auth application-default login`
3. Terraform commands - `init`, `plan`, `apply`
4. Create cloud blocks - `poetry run python blocks/make_gcp_blocks.py`
5. Run the flows - `poetry run python flows/elt_bq_to_gcs.py`
6. Create dashboard using Looker studio
7. Cleanup - `terraform destroy`
