from pydantic import BaseModel
from datetime import datetime

class EnterpriseOUT(BaseModel):
    id: int
    name: str
    description: str | None
    website_url: str | None
    logo_url: str | None
    user_id: int
    industry_id: int
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True

