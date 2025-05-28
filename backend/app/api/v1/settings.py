from fastapi import APIRouter, Depends, Body
from app.api.deps import get_current_user
from app.models.user import User
from typing import Optional

router = APIRouter()

# Update user profile info
@router.put("/profile")
async def update_profile(
    full_name: Optional[str] = Body(None),
    avatar_url: Optional[str] = Body(None),
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "updated": {
            "full_name": full_name,
            "avatar_url": avatar_url
        }
    }

# Change password or enable 2FA
@router.post("/security")
async def update_security_settings(
    new_password: Optional[str] = Body(None),
    enable_2fa: Optional[bool] = Body(False),
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "2fa_enabled": enable_2fa,
        "password_changed": bool(new_password)
    }

# Notification preferences
@router.put("/notifications")
async def update_notifications(
    email_alerts: bool = Body(...),
    push_alerts: bool = Body(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "email_alerts": email_alerts,
        "push_alerts": push_alerts
    }

# Billing & plan
@router.get("/billing")
async def get_billing_info(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "plan": "Pro",
        "storage_used": "12.4 GB",
        "next_billing_date": "2025-06-01"
    }

# Cloud drive integrations
@router.post("/cloud-integration")
async def link_cloud_drive(
    provider: str = Body(...),  # drive, dropbox, onedrive
    token: str = Body(...),
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "linked_provider": provider
    }

# Export account data
@router.get("/export")
async def export_account_data(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "status": "export_started"
    }

# UI preferences
@router.put("/preferences")
async def update_preferences(
    theme: Optional[str] = Body("light"),
    language: Optional[str] = Body("en"),
    date_format: Optional[str] = Body("YYYY-MM-DD"),
    layout: Optional[str] = Body("grid"),
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "preferences": {
            "theme": theme,
            "language": language,
            "date_format": date_format,
            "layout": layout
        }
    }
