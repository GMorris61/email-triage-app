import json
import os
import boto3
from google.oauth2.credentials import Credentials

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
