import argparse
import configparser
import re

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect_gcp import GcpCredentials, BigQueryWarehouse, GcsBucket

from dbt_bq_processing import trigger_dbt_flow

gcp_credentials = GcpCredentials.load("gcp-github-repos-block")


@task(name="Export the BigQuery dataset to GCS")
def bigquery_export_to_gcs(project: str, gcs_name: str, dataset: str) -> None:
    with BigQueryWarehouse(gcp_credentials=gcp_credentials) as warehouse:
        warehouse.execute(
            "EXPORT DATA OPTIONS ( "
            f"uri='gs://{gcs_name}/input/*.parquet', "
            "format='PARQUET', "
            "overwrite=true ) AS "
            f"SELECT * FROM {project}.{dataset}.sample_repos__file_contents_last_updated"
        )


@task(name="Upload PySpark processing script to GCS")
def upload_pyspark_script_to_gcs(gcs_name: str) -> None:
    gcs_bucket = GcsBucket(
        bucket=gcs_name
    )

    gcs_bucket.upload_from_path("process_data.py", "scripts/process_data.py")


@task(name="Submit Dataproc job to process Parquet files on GCS")
def submit_dataproc_job(project: str, gcs_name:str, cluster_name: str) -> None:
    job_client = dataproc.JobControllerClient(
        client_options={"api_endpoint": "us-central1-dataproc.googleapis.com:443"}
    )

    job = {
            "placement": {"cluster_name": cluster_name},
            "pyspark_job": {
                "main_python_file_uri": f"gs://{gcs_name}/scripts/process_data.py",
                "args": [f"--input=gs://{gcs_name}/input/*", f"--output=gs://{gcs_name}/output"]
            },
        }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project, "region": "us-central1", "job": job}
    )
    response = operation.result()
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client(project=project)
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_string()
    )

    print(f"Job finished successfully: {output}")


@task(name="Create hive partitioned table in BigQuery")
def bigquery_create_external_table(project: str, gcs_name: str, dataset: str) -> None:
    with BigQueryWarehouse(gcp_credentials=gcp_credentials) as warehouse:
        warehouse.execute(
            "CREATE EXTERNAL TABLE "
            f"{project}.{dataset}.hive_partitioned_table "
            "WITH PARTITION COLUMNS ( "
            "year INT64, "
            "month INT64, "
            "date INT64 ) "
            "OPTIONS ( "
            f"uris = ['gs://{gcs_name}/output/*'], "
            "format = 'PARQUET', "
            f"hive_partition_uri_prefix = 'gs://{gcs_name}/output', "
            "require_hive_partition_filter = false);"
        )


@flow(name="ELT Flow", task_runner=SequentialTaskRunner())
def extract_load_transform(project: str, gcs_name: str, dataset: str, cluster_name: str) -> None:
    bigquery_export_to_gcs(project, gcs_name, dataset)
    upload_pyspark_script_to_gcs(gcs_name)
    submit_dataproc_job(project, gcs_name, cluster_name)
    bigquery_create_external_table(project, gcs_name, dataset)


@flow(name="Parent Flow", task_runner=SequentialTaskRunner())
def parent_flow(project: str, gcs_name: str, dataset: str, cluster_name: str, test_run: bool) -> None:
    trigger_dbt_flow(test_run)
    extract_load_transform(project, gcs_name, dataset, cluster_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Load and Transform the BigQuery Dataset")
    parser.add_argument("--test", action="store_true", help="Test run to create sample dataset")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read("vars.conf")
    parent_flow(
        config["variables"]["project"], 
        config["variables"]["data_lake_bucket_name"], 
        config["variables"]["bq_dataset"], 
        config["variables"]["dataproc_cluster"], 
        args.test
    )
