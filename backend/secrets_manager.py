import json
import os
import urllib.request
from typing import Optional
import boto3
from google.oauth2.credentials import Credentials


def _detect_region_from_ec2_metadata() -> Optional[str]:
    """Best-effort region detection on EC2 via IMDS; returns None if unavailable."""
    try:
        req = urllib.request.Request(
            "http://169.254.169.254/latest/dynamic/instance-identity/document"
        )
        with urllib.request.urlopen(req, timeout=1) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        region = payload.get("region")
        return region if isinstance(region, str) and region else None
    except Exception:
        return None

# -----------------------------
# RETRIEVE SECRET FROM AWS
# -----------------------------
def get_gmail_credentials() -> Credentials:
    """
    Retrieve Gmail OAuth credentials stored in AWS Secrets Manager
    and return a Credentials object usable by the Gmail API client.
    """
    # Configurable via environment variables (with sensible defaults)
    # - GMAIL_SECRET_NAME: AWS Secrets Manager secret name containing Gmail OAuth JSON
    # - AWS_REGION / AWS_DEFAULT_REGION: region for Secrets Manager
    secret_name = os.getenv("GMAIL_SECRET_NAME", "gmail-credentials")
    region_name = (
        os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or os.getenv("GMAIL_SECRET_REGION")
        or _detect_region_from_ec2_metadata()
        or "us-east-1"
    )

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    # Retrieve the secret value
    response = client.get_secret_value(SecretId=secret_name)

    # The secret is stored as a JSON string
    secret_string = response["SecretString"]
    token_data = json.loads(secret_string)

    # Convert the JSON token data into a Credentials object
    creds = Credentials.from_authorized_user_info(token_data)

    return creds
