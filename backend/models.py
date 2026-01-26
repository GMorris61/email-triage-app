from pydantic import BaseModel
from typing import List, Optional

# -----------------------------
# MODEL FOR A SINGLE EMAIL ITEM
# -----------------------------
class EmailItem(BaseModel):
    id: str
    sender: str
    subject: str

# -----------------------------
# SEARCH RESPONSE MODEL
# -----------------------------
class SearchResponse(BaseModel):
    keyword: str
    results: List[EmailItem]

# -----------------------------
# ACTION REQUEST MODEL
# -----------------------------
class ActionRequest(BaseModel):
    email_ids: List[str]
    action: str  # "trash", "archive", or "dry-run"

# -----------------------------
# ACTION RESPONSE MODEL
# -----------------------------
class ActionResponse(BaseModel):
    action: str
    affected_emails: List[str]
    result: Optional[str]  # message returned from Gmail service
