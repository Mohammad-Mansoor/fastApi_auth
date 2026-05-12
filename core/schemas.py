from pydantic import BaseModel
from typing import Optional


class QueryOptionsDto(BaseModel):

    # =====================================================
    # PAGINATION
    # =====================================================

    page: Optional[int] = 1
    limit: Optional[int] = 10

    # =====================================================
    # SEARCH
    # =====================================================

    search: Optional[str] = None

    # =====================================================
    # SORTING
    # =====================================================

    # Example:
    # firstName:ASC
    # createdAt:DESC
    sort: Optional[str] = None

    # =====================================================
    # CURSOR PAGINATION
    # =====================================================

    cursor: Optional[str] = None

    # =====================================================
    # LANGUAGE FOR JSONB TRANSLATIONS
    # =====================================================

    lang: Optional[str] = "en"


class Headers(BaseModel):
    fingerprint: str
    device_name: str
    device_type: str
    os: str
    browser: str
    client_id: str
    
    
class Meta(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int
    hasNextPage: bool
    hasPreviousPage: bool
    model_config = {
        "from_attributes": True
    }