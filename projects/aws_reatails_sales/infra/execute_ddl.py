from pathlib import Path
import sys
import time

# ----------------------------------------------------------
# Add project root to Python path
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ----------------------------------------------------------
# Imports
# ----------------------------------------------------------

from infra.common import get_athena_client
from infra.config_loader import load_environment

env = load_environment()
athena = get_athena_client()

# ----------------------------------------------------------
# DDL Directory
# ----------------------------------------------------------

DDL_DIR = PROJECT_ROOT / env.DDL_DIR

print(f"Loaded environment : {env.ENV}")
print(f"Project Root       : {PROJECT_ROOT}")
print(f"DDL Directory      : {DDL_DIR}")

if not DDL_DIR.exists():
    raise FileNotFoundError(f"DDL directory not found: {DDL_DIR}")


# ==========================================================
# Execute Athena DDL
# ==========================================================

def execute_sql(sql_file):

    sql_path = DDL_DIR / sql_file

    print(f"\nLooking for: {sql_path}")

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    sql = sql_path.read_text(encoding="utf-8")

    # ------------------------------------------------------
    # Replace placeholders
    # ------------------------------------------------------

    sql = (
        sql.replace("${DATA_LAKE_BUCKET}", env.DATA_LAKE_BUCKET)
           .replace("${RAW_PREFIX}", env.RAW_PREFIX.rstrip("/"))
           .replace("${BRONZE_PREFIX}", env.BRONZE_PREFIX.rstrip("/"))
    )

    print(f"\nExecuting {sql_file}...")

    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={
            "Database": "default"
        },
        ResultConfiguration={
            "OutputLocation": (
                f"s3://{env.DATA_LAKE_BUCKET}/"
                f"{env.ATHENA_RESULTS_PREFIX}"
            )
        },
    )

    query_execution_id = response["QueryExecutionId"]

    print(f"QueryExecutionId : {query_execution_id}")

    while True:

        execution = athena.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        status = execution["QueryExecution"]["Status"]["State"]

        if status in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break

        print(f"Status : {status}")

        time.sleep(2)

    if status != "SUCCEEDED":

        reason = execution["QueryExecution"]["Status"].get(
            "StateChangeReason",
            "Unknown Error"
        )

        raise RuntimeError(
            f"""
Execution Failed

SQL File : {sql_file}
Status   : {status}
Reason   : {reason}
"""
        )

    print(f"✓ {sql_file} executed successfully.")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("\nDeploying Athena DDLs...\n")

    execute_sql("raw_sales.sql")

    print("\nAll DDLs executed successfully.")