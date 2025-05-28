from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Literal

# ----- Linked External Drives -----
class LinkedDrive(BaseModel):
    id: UUID
    user_id: UUID
    provider: Literal['google_drive', 'dropbox', 'icloud', 'onedrive', 'mega', 'jottacloud']
    access_token: str
    refresh_token: Optional[str]
    expires_at: Optional[datetime]
    linked_at: datetime
    status: str  # 'active', 'revoked', 'expired'

# ----- Mounted Folder (Virtual Mount) -----
class ExternalMount(BaseModel):
    id: UUID
    user_id: UUID
    linked_drive_id: UUID
    remote_path: str
    local_mount_path: str  # where it appears in Stratos
    sync_mode: Literal['mirror', 'one_way', 'manual']
    mounted_at: datetime
    is_active: bool = True

# ----- Import Rules (Auto-sync or copy) -----
class ImportRule(BaseModel):
    id: UUID
    user_id: UUID
    mount_id: UUID
    match_pattern: Optional[str]  # e.g. *.pdf or folders/*
    action: Literal['import', 'ignore', 'tag', 'convert']
    destination_folder_id: Optional[UUID]
    created_at: datetime
