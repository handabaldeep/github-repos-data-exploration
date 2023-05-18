from prefect import flow
from prefect_dbt.cli.commands import DbtCoreOperation

@flow(name="dbt transformation Flow")
def trigger_dbt_flow(test_run: bool) -> str:
    build_command = "dbt build"
    if not test_run:
        build_command = build_command + " --vars 'is_test_run: false'"
    result = DbtCoreOperation(
        commands = ["dbt debug", 
                    build_command],
        project_dir = "dbt_github_repos",
        profiles_dir = "."
    ).run()

    return result
