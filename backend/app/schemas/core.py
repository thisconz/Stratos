from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# ----- Bucket -----
class StratosCoreBucket(BaseModel):
    id: UUID
    bucket_name: str
    region: str
    storage_class: str
    user_id: UUID
    created_at: datetime

# ----- File -----
class FileMetadata(BaseModel):
    id: UUID
    user_id: UUID
    parent_folder_id: Optional[UUID]
    name: str
    extension: str
    mime_type: str
    size: int
    path: str
    is_deleted: bool = False
    is_starred: bool = False
    created_at: datetime
    updated_at: datetime

# ----- Folder -----
class FolderMetadata(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    parent_folder_id: Optional[UUID]
    path: str
    created_at: datetime
    updated_at: datetime

# ----- Versioning -----
class FileVersion(BaseModel):
    id: UUID
    file_id: UUID
    version_number: int
    object_key: str
    hash: str
    size: int
    created_at: datetime

# ----- Chunked Blocks -----
class FileBlock(BaseModel):
    id: UUID
    file_id: UUID
    block_index: int
    hash: str
    data_ref: str
    size: int
    created_at: datetime

