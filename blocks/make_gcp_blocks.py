import sys

from prefect_gcp import GcpCredentials, GcsBucket


def create_gcp_blocks(gcs_bucket: str) -> None:
    credentials_block = GcpCredentials(
        service_account_file="service-account.json",
    )
    credentials_block.save("gcp-github-repos-block", overwrite=True)

    bucket_block = GcsBucket(
        gcp_credentials=GcpCredentials.load("gcp-github-repos-block"),
        bucket=gcs_bucket,
    )
    bucket_block.save("gcp-github-repos-bucket-block", overwrite=True)


if __name__ == "__main__":
    create_gcp_blocks(sys.argv[1])
