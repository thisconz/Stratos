from fastapi import APIRouter, Depends, Body
from app.api.deps import get_current_user
from app.models.user import User
from typing import List, Optional

router = APIRouter()

# Share file with users by email
@router.post("/share/{file_id}")
async def share_file(
    file_id: str,
    emails: List[str] = Body(...),
    permission: str = Body(...),  # "viewer", "commenter", "editor"
    current_user: User = Depends(get_current_user)
):
    return {
        "file_id": file_id,
        "shared_with": emails,
        "permission": permission,
        "status": "success"
    }

# Generate or update shareable link
@router.post("/link/{file_id}")
async def create_share_link(
    file_id: str,
    password: Optional[str] = Body(None),
    expiry_date: Optional[str] = Body(None),
    branding: Optional[str] = Body(None),
    current_user: User = Depends(get_current_user)
):
    return {
        "file_id": file_id,
        "link": f"https://stratos.app/s/{file_id}",
        "protected": bool(password),
        "expires": expiry_date,
        "branding": branding
    }

# Get activity feed for file
@router.get("/activity/{file_id}")
async def file_activity_feed(file_id: str, current_user: User = Depends(get_current_user)):
    return {
        "file_id": file_id,
        "activity": [
            {"action": "shared", "by": current_user.email, "timestamp": "..."},
            {"action": "commented", "by": "user2@example.com", "timestamp": "..."}
        ]
    }

# Revoke share access
@router.delete("/revoke/{file_id}")
async def revoke_file_access(
    file_id: str,
    user_email: str = Body(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "file_id": file_id,
        "revoked": user_email,
        "status": "success"
    }
