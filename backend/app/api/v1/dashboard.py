from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/quick-access")
async def get_quick_access(current_user: User = Depends(get_current_user)):
    return {
        "recent": [],
        "starred": [],
        "modified": []
    }

@router.get("/navigation")
async def get_navigation_sidebar(current_user: User = Depends(get_current_user)):
    return {
        "sections": [
            "my_files",
            "shared_with_me",
            "vision_search",
            "synced_devices",
            "trash",
            "settings"
        ]
    }

@router.get("/storage-status")
async def get_storage_status(current_user: User = Depends(get_current_user)):
    return {
        "used": "4.3 GB",
        "total": "15 GB",
        "percent": 28.7
    }
