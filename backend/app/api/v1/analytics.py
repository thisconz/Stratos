from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# Usage dashboard
@router.get("/usage")
async def get_usage_dashboard(current_user: User = Depends(get_current_user)):
    return {
        "total_files": 1823,
        "total_storage": "357 GB",
        "bandwidth_used": "21 GB",
        "top_contributors": [
            {"user": "alice", "files": 423},
            {"user": "bob", "files": 371}
        ],
        "file_type_distribution": {
            "pdf": 340,
            "jpg": 290,
            "mp4": 170,
            "docx": 210
        },
        "vision_usage": {
            "ocr_calls": 182,
            "tags_generated": 842
        }
    }

# Alerts
@router.get("/alerts")
async def get_alerts(current_user: User = Depends(get_current_user)):
    return {
        "alerts": [
            {"type": "sync_error", "file": "invoice_2031.pdf", "device": "Macbook Pro"},
            {"type": "storage_threshold", "level": "85%"},
            {"type": "shared_link_access", "file": "presentation.mp4", "ip": "103.21.44.1"}
        ]
    }
