from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class MetadataSearchQuery(BaseModel):
    exact: Optional[Dict[str, str]] = None
    partial: Optional[Dict[str, str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = 1
    page_size: int = 20

class FileOut(BaseModel):
    id: int
    object_key: str
    filename: str
    version_number: int
    size: int
    uploaded_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    owner_id: Optional[int] = None
    access_count: Optional[int] = None
    deleted: Optional[bool] = None