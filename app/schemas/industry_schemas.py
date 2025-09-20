from pydantic import BaseModel
from datetime import datetime

class IndustryOUT(BaseModel):
    id: int
    name: str
    description: str | None
    icon_url: str | None
    is_active: bool
    usage_count: int
    user_id: int
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True

class CreateIndustryDTO(BaseModel):
    name: str
    description: str | None
    icon_url: str | None

    def to_entity(self):
        from app.configs.db.database import IndustryEntity

        return IndustryEntity(
            name = self.name,
            description = self.description,
            icon_url = self.icon_url,
        )

class UpdateIndustryDTO(BaseModel):
    name: str | None
    description: str | None
    icon_url: str | None
    is_active: bool | None
