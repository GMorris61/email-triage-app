from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import EmailItem
from secrets_manager import get_gmail_credentials

# -----------------------------
# BUILD GMAIL SERVICE CLIENT
# -----------------------------
def get_gmail_service():
    """
    Build and return an authenticated Gmail API service client
    using credentials from AWS Secrets Manager.
    """
    creds: Credentials = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service


# -----------------------------
# SEARCH EMAILS
# -----------------------------
def search_emails(keyword: str, max_results: int = 10) -> List[EmailItem]:
    """
    Search for emails where the subject contains the given keyword.
    Returns up to max_results EmailItem objects.
    """
    try:
        service = get_gmail_service()

        # Gmail search query: subject contains keyword
        query = f"subject:{keyword}"

        response = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )

        messages = response.get("messages", [])
        results: List[EmailItem] = []

        for msg in messages:
            msg_id = msg["id"]
            msg_detail = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="metadata", metadataHeaders=["From", "Subject"])
                .execute()
            )

            headers = msg_detail.get("payload", {}).get("headers", [])
            sender = _get_header_value(headers, "From")
            subject = _get_header_value(headers, "Subject")

            results.append(
                EmailItem(
                    id=msg_id,
                    sender=sender,
                    subject=subject,
                )
            )

        return results

    except HttpError as e:
        # You can log this in a real app
        raise Exception(f"Gmail API error during search: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during search: {e}")


# -----------------------------
# PERFORM ACTION ON EMAILS
# -----------------------------
def perform_action(email_ids: List[str], action: str) -> str:
    """
    Perform an action on a list of email IDs.
    Supported actions: "trash", "archive", "dry-run".
    """
    try:
        service = get_gmail_service()

        if action == "dry-run":
            # Do not modify anything, just describe what would happen
            return f"Dry-run: would apply '{action}' to {len(email_ids)} emails."

        if action == "trash":
            for msg_id in email_ids:
                service.users().messages().trash(userId="me", id=msg_id).execute()
            return f"Trashed {len(email_ids)} emails."

        if action == "archive":
            # Archive = remove INBOX label
            body = {"removeLabelIds": ["INBOX"]}
            for msg_id in email_ids:
                service.users().messages().modify(userId="me", id=msg_id, body=body).execute()
            return f"Archived {len(email_ids)} emails."

        # If action is not recognized
        raise ValueError(f"Unsupported action: {action}")

    except HttpError as e:
        raise Exception(f"Gmail API error during action '{action}': {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during action '{action}': {e}")


# -----------------------------
# HELPER: GET HEADER VALUE
# -----------------------------
def _get_header_value(headers: List[Dict[str, Any]], name: str) -> str:
    """
    Extract a specific header value (e.g., From, Subject) from Gmail message headers.
    """
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""
