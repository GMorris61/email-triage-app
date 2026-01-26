from fastapi import APIRouter, HTTPException
from typing import List
from models import SearchResponse, ActionRequest, ActionResponse
from gmail_service import search_emails, perform_action

# Create a router object that will hold all email-related endpoints
router = APIRouter(
    prefix="/email",
    tags=["Email Operations"]
)

# -----------------------------
# SEARCH ENDPOINT
# -----------------------------
@router.get("/search", response_model=SearchResponse)
def search_emails_route(keyword: str):
    """
    Search Gmail for emails where the subject contains the keyword.
    Returns up to 10 matching emails.
    """
    try:
        results = search_emails(keyword)
        return SearchResponse(
            keyword=keyword,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# ACTION ENDPOINT
# -----------------------------
@router.post("/action", response_model=ActionResponse)
def action_route(request: ActionRequest):
    """
    Perform an action (trash, archive, dry-run) on selected emails.
    """
    try:
        result = perform_action(
            email_ids=request.email_ids,
            action=request.action
        )
        return ActionResponse(
            action=request.action,
            affected_emails=request.email_ids,
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
