from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# ----- Shared Links -----
class SharedLink(BaseModel):
    id: UUID
    file_id: UUID
    user_id: UUID
    link_token: str
    permissions: str  # 'read', 'write', 'comment', etc.
    expires_at: Optional[datetime]
    password_protected: bool = False
    created_at: datetime

# ----- User-to-User File Share -----
class FileShare(BaseModel):
    id: UUID
    file_id: UUID
    owner_id: UUID
    target_user_id: UUID
    permissions: str  # 'read', 'write', 'comment'
    created_at: datetime

# ----- File Access Logs -----
class AuditLog(BaseModel):
    id: UUID
    file_id: UUID
    user_id: Optional[UUID]  # could be anonymous for public links
    action: str  # 'viewed', 'downloaded', 'edited', etc.
    device_id: Optional[UUID]
    ip_address: Optional[str]
    timestamp: datetime

# ----- Permission Rule (optional) -----
class AccessRule(BaseModel):
    id: UUID
    target_id: UUID  # file or folder
    user_id: UUID
    can_read: bool
    can_write: bool
    can_comment: bool
    can_reshare: bool
    created_at: datetime
