import sys

from google.cloud import dataproc_v1
from google.cloud import storage
from google.oauth2 import service_account
from prefect import flow, task
from prefect_gcp import GcpCredentials, BigQueryWarehouse, GcsBucket


@task
def bigquery_export_to_gcs(gcs_uri: str):
    gcp_credentials = GcpCredentials.load("gcp_github_repos_block")

    with BigQueryWarehouse(gcp_credentials=gcp_credentials) as warehouse:
        warehouse.execute(
            "EXPORT DATA OPTIONS("
            f"uri='{gcs_uri}',"
            "format='PARQUET',"
            "overwrite=true) AS"
            "SELECT * FROM github-repos-data-exploration.dbt_github_repos.sample_repos__file_contents_last_updated"
        )


@task
def upload_pyspark_script_to_gcs(gcs_uri: str):
    gcp_credentials = GcpCredentials.load("gcp_github_repos_block")

    gcs_bucket = GcsBucket(
        bucket=gcs_uri,
        gcp_credentials=gcp_credentials
    )

    gcs_bucket.upload_from_path("process_data.py")


@task
def submit_dataproc_job():
    credentials = service_account.Credentials.from_service_account_file("service-account.json")
    



@flow
def extract_load_transform():
    bigquery_export_to_gcs(sys.argv[1])
    upload_pyspark_script_to_gcs(sys.argv[1])



if __name__ == "__main__":
    extract_load_transform()
