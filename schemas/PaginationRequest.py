from pydantic import BaseModel, Field
from typing import Optional

class PaginationRequest(BaseModel):
    limit: Optional[int] = Field(10, ge=0)
    offset: Optional[int] = Field(0, ge=0)
    categories: Optional[str] = Field(None, min_length=3)
    company: Optional[str] = Field(None, min_length=3)
