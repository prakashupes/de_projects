"""
Common AWS utilities used across infrastructure scripts.
"""

import boto3
from botocore.exceptions import ClientError

from config.dev import AWS_REGION


# ==========================================================
# AWS Session
# ==========================================================

def get_session():
    """
    Returns a boto3 session.
    """
    return boto3.Session(region_name=AWS_REGION)


# ==========================================================
# AWS Clients
# ==========================================================

def get_s3_client():
    """
    Returns an S3 client.
    """
    return get_session().client("s3")


def get_glue_client():
    """
    Returns a Glue client.
    """
    return get_session().client("glue")


def get_athena_client():
    """
    Returns an Athena client.
    """
    return get_session().client("athena")


def get_iam_client():
    """
    Returns an IAM client.
    """
    return get_session().client("iam")


# ==========================================================
# AWS Resources
# ==========================================================

def get_s3_resource():
    """
    Returns an S3 resource.
    """
    return get_session().resource("s3")


# ==========================================================
# Utility Functions
# ==========================================================

def bucket_exists(bucket_name: str) -> bool:
    """
    Check whether an S3 bucket exists.
    """

    s3 = get_s3_client()

    try:
        s3.head_bucket(Bucket=bucket_name)
        return True

    except ClientError:
        return False