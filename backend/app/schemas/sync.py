from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# ----- File Sync Status -----
class StratosSync(BaseModel):
    id: UUID
    user_id: UUID
    file_id: UUID
    device_id: UUID
    status: str  # e.g. 'synced', 'pending', 'conflict'
    synced_at: datetime

# ----- Registered Devices -----
class SyncDevice(BaseModel):
    id: UUID
    user_id: UUID
    device_name: str
    device_type: str  # e.g. 'desktop', 'mobile'
    os: str
    last_seen: datetime
    created_at: datetime

# ----- Sync Job Tracking -----
class SyncJob(BaseModel):
    id: UUID
    user_id: UUID
    job_type: str  # e.g. 'full_sync', 'partial_sync'
    status: str  # e.g. 'running', 'completed'
    files_synced: int
    started_at: datetime
    completed_at: Optional[datetime]

# ----- Version Conflict -----
class SyncConflict(BaseModel):
    id: UUID
    file_id: UUID
    device_id: UUID
    conflict_type: str  # e.g. 'simultaneous_edit'
    local_version_id: UUID
    remote_version_id: UUID
    resolved: bool = False
    resolved_at: Optional[datetime]

# ----- Per-device Sync State -----
class SyncVersionState(BaseModel):
    id: UUID
    file_id: UUID
    device_id: UUID
    last_version_id: UUID
    synced_at: datetime
