from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# ----- OCR Extraction -----
class DocumentOCR(BaseModel):
    id: UUID
    file_id: UUID
    user_id: UUID
    language: str
    content: str
    extracted_at: datetime

# ----- Text Block with Bounding Boxes -----
class OCRBlock(BaseModel):
    id: UUID
    ocr_id: UUID
    text: str
    page_number: int
    bbox: List[float]  # [x, y, width, height]
    confidence: float

# ----- Smart Tags (AI or manual) -----
class SmartTag(BaseModel):
    id: UUID
    file_id: UUID
    user_id: UUID
    tag: str
    confidence: Optional[float]
    source: str  # 'ai', 'user', 'import'
    created_at: datetime

# ----- Indexed Search Metadata -----
class SearchIndex(BaseModel):
    id: UUID
    file_id: UUID
    user_id: UUID
    title: Optional[str]
    keywords: List[str]
    summary: Optional[str]
    indexed_at: datetime
