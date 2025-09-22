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

class CreateEnterpriseDTO(BaseModel):
    name: str
    description: str | None
    website_url: str | None
    logo_url: str | None

    def to_entity(self):
        from app.configs.db.database import EnterpriseEntity

        return EnterpriseEntity(
            name = self.name,
            description = self.description,
            website_url = self.website_url,
            logo_url = self.logo_url,
        )

class UpdateEnterpriseDTO(BaseModel):
    name: str | None
    description: str | None
    website_url: str | None
    logo_url: str | None
    industry_id: int | None