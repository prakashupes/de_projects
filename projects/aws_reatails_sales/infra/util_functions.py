from pathlib import Path
import sys
import os
# ----------------------------------------------------------
# Add project root to Python path
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ----------------------------------------------------------
# Imports
# ----------------------------------------------------------

from infra.common import get_s3_client, bucket_exists
from infra.config_loader import load_environment

env = load_environment()
s3 = get_s3_client()

print(f"Loaded environment: {env}")


# ==========================================================
# Create Bucket
# ==========================================================

def create_bucket():

    bucket = env.DATA_LAKE_BUCKET

    print(f"Deploying infrastructure to {bucket}")

    if bucket_exists(bucket):
        print(f"Bucket '{bucket}' already exists.")
        return

    print(f"Creating bucket '{bucket}'...")

    s3.create_bucket(Bucket=bucket)

    print("Bucket created successfully.")


# ==========================================================
# Create Folder Structure
# ==========================================================

def create_folders():

    folders = [
        env.RAW_PREFIX,
        env.BRONZE_PREFIX,
        env.SILVER_PREFIX,
        env.GOLD_PREFIX,
        env.SCRIPT_PREFIX,
        env.DDL_PREFIX,
        env.ATHENA_RESULTS_PREFIX,
        env.TEMP_PREFIX,
    ]

    for folder in folders:

        print(f"Creating {folder}")

        s3.put_object(
            Bucket=env.DATA_LAKE_BUCKET,
            Key=folder,
        )

    print("Folder structure created.")


# ==========================================================
# Upload Directory
# ==========================================================

def upload_directory(local_folder, s3_prefix, extension):

    local_folder = Path(local_folder)

    if not local_folder.exists():
        print(f"{local_folder} not found.")
        return

    for file in local_folder.glob(f"*.{extension}"):

        print(f"Uploading {file.name}")

        s3.upload_file(
            str(file),
            env.DATA_LAKE_BUCKET,
            f"{s3_prefix}{file.name}",
        )

    print(f"{extension.upper()} upload completed.")


# ==========================================================
# Deploy Infrastructure
# ==========================================================

def deploy():

    create_bucket()

    create_folders()

    upload_directory(
        env.GLUE_SCRIPT_DIR,
        env.SCRIPT_PREFIX,
        "py",
    )

    upload_directory(
        env.DDL_DIR,
        env.DDL_PREFIX,
        "sql",
    )

    upload_directory(
        env.DATA_GENERATOR_DIR,
        env.RAW_PREFIX,
        "csv",
    )

    print("\nInfrastructure deployment completed.")


if __name__ == "__main__":

    print("Starting infrastructure deployment...\n")
    print(env.DATA_LAKE_BUCKET)
    #create_folders()
    print(os.system(f"aws s3 ls s3://{env.DATA_LAKE_BUCKET}"))
    partition = "year=2026/month=06/day=30"

    cmd = (
        f"aws s3 cp "
        f"projects/aws_reatails_sales/data_generator/sample_data "
        f"s3://{env.DATA_LAKE_BUCKET}/raw/{partition}/ "
        f"--recursive"
    )

    print(cmd)
    os.system(cmd)