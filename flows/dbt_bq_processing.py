import sys

from prefect import flow
from prefect_dbt.cli.commands import DbtCoreOperation

@flow
def trigger_dbt_flow(test_run=False) -> str:
    result = DbtCoreOperation(
        # if test_run:
        # commands = ["dbt debug", "dbt run"],
        commands = ["dbt debug"],
        project_dir = "dbt_github_repos",
        profiles_dir = "."
    ).run()
    return result

if __name__ == "__main__":
    trigger_dbt_flow(sys.argv[1])
