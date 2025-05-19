# File metadata schemas
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class MetadataSearchQuery(BaseModel):
    exact: Optional[Dict[str, str]] = None
    partial: Optional[Dict[str, str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = 1
    page_size: int = 20