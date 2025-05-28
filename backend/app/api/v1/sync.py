from fastapi import APIRouter, Depends, Form
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# Sync Configuration
@router.get("/config")
async def get_sync_config(current_user: User = Depends(get_current_user)):
    return {"sync_mode": "auto", "bandwidth_limit": "unlimited", "cpu_limit": "normal"}

@router.post("/config")
async def update_sync_config(
    sync_mode: str = Form(...),
    bandwidth_limit: str = Form(...),
    cpu_limit: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    return {"status": "updated", "sync_mode": sync_mode}

# Folder Selection
@router.post("/folders/select")
async def select_sync_folders(folders: list[str] = Form(...), current_user: User = Depends(get_current_user)):
    return {"folders_selected": folders}

# Conflict Handling
@router.post("/conflicts")
async def handle_conflict(
    file_id: str = Form(...),
    resolution_strategy: str = Form(...),  # "keep_both", "replace", "manual"
    current_user: User = Depends(get_current_user)
):
    return {"file_id": file_id, "resolution": resolution_strategy}

# Devices
@router.get("/devices")
async def list_connected_devices(current_user: User = Depends(get_current_user)):
    return {"devices": []}

@router.delete("/devices/{device_id}")
async def revoke_device_access(device_id: str, current_user: User = Depends(get_current_user)):
    return {"status": "revoked", "device_id": device_id}

@router.get("/devices/{device_id}/history")
async def get_device_sync_history(device_id: str, current_user: User = Depends(get_current_user)):
    return {"device_id": device_id, "history": []}
