import json
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
    secret_name = "gmail-credentials"  # Replace with your actual secret name
    region_name = "us-east-1"           # Replace with your region if different

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
