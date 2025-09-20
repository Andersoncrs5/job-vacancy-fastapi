from pydantic import BaseModel
from datetime import datetime

class IndustryOUT(BaseModel):
    id: int
    name: str
    icon_url: str | None
    is_active: bool
    usage_count: int
    user_id: int
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True