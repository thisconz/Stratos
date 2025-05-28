from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ----- Storage Usage Per User -----
class StorageStats(BaseModel):
    id: UUID
    user_id: UUID
    total_files: int
    total_folders: int
    total_size: int  # in bytes
    updated_at: datetime

# ----- Activity Log -----
class ActivityLog(BaseModel):
    id: UUID
    user_id: UUID
    action: str  # 'upload', 'delete', 'share', etc.
    target_id: Optional[UUID]
    target_type: Optional[str]  # 'file', 'folder'
    ip_address: Optional[str]
    device_id: Optional[UUID]
    timestamp: datetime

# ----- Plan & Billing Info -----
class BillingRecord(BaseModel):
    id: UUID
    user_id: UUID
    plan_name: str
    amount_cents: int
    currency: str
    period_start: datetime
    period_end: datetime
    payment_method: str
    paid_at: datetime
