from prefect import flow
from prefect_gcp import GcpCredentials

@flow
def create_gcp_block():
    with open("service-account.json") as f:
        service_account = f.read()

    block = GcpCredentials(
        service_account_info=service_account,
        project="github-repos-data-exploration"
    )

    block.save("gcp_github_repos_block")

if __name__ == "__main__":
    create_gcp_block()
