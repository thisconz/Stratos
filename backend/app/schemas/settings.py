from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

# ----- User Settings -----
class UserSettings(BaseModel):
    id: UUID
    user_id: UUID
    theme: Optional[str]  # 'light', 'dark', 'system'
    language: Optional[str]
    time_zone: Optional[str]
    date_format: Optional[str]  # 'MM/DD/YYYY', 'DD/MM/YYYY', etc.
    default_view: Optional[str]  # 'list', 'grid'
    created_at: datetime
    updated_at: datetime

# ----- Feature Flags & Plugin Toggles -----
class FeatureFlags(BaseModel):
    id: UUID
    user_id: UUID
    flags: Dict[str, bool]  # e.g. {'stratos_vision': True, 'stratos_sync': False}
    created_at: datetime
    updated_at: datetime

# ----- System Config (Admin only) -----
class SystemConfig(BaseModel):
    id: UUID
    key: str
    value: str
    description: Optional[str]
    updated_at: datetime
