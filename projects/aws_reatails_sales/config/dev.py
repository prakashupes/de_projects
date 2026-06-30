"""
Development Environment Configuration
"""

# ==========================================================
# Environment
# ==========================================================

ENV = "dev"

AWS_REGION = "us-east-1"

AWS_ACCOUNT_ID = "<YOUR_AWS_ACCOUNT_ID>"


# ==========================================================
# S3 Configuration
# ==========================================================

DATA_LAKE_BUCKET = "retail-data-lake-dev"
DATA_LAKE_BUCKET_ARN = "arn:aws:s3:::retail-data-lake-dev"
# Bucket Names
SCRIPT_BUCKET = DATA_LAKE_BUCKET
DDL_BUCKET = DATA_LAKE_BUCKET

# S3 Prefixes
RAW_PREFIX = "raw/"
BRONZE_PREFIX = "bronze/"
SILVER_PREFIX = "silver/"
GOLD_PREFIX = "gold/"

SCRIPT_PREFIX = "scripts/"
DDL_PREFIX = "ddl/"
ATHENA_RESULTS_PREFIX = "athena-results/"
TEMP_PREFIX = "temp/"


# ==========================================================
# Glue Configuration
# ==========================================================

GLUE_CATALOG_NAME = "320489876642"
GLUE_DATABASE_NAME = "retail_dev"
GLUE_ROLE = "AWSGlueServiceRole-Retail"

GLUE_VERSION = "5.0"

WORKER_TYPE = "G.1X"

NUMBER_OF_WORKERS = 2

TEMP_DIR = f"s3://{DATA_LAKE_BUCKET}/{TEMP_PREFIX}"


# ==========================================================
# Athena Configuration
# ==========================================================

ATHENA_WORKGROUP = "primary"

ATHENA_OUTPUT_LOCATION = (
    f"s3://{DATA_LAKE_BUCKET}/{ATHENA_RESULTS_PREFIX}"
)


# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"


# ==========================================================
# Local Project Paths
# ==========================================================

TABLE_CONFIG_DIR = "table_configs"

DDL_DIR = "athena_ddls"

GLUE_SCRIPT_DIR = "glue"

DATA_GENERATOR_DIR = "data_generator/sample_data"