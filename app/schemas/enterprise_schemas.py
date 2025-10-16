from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel

class EnterpriseOUT(ORJSONModel):
    id: int
    name: str
    description: str | None
    website_url: str | None
    logo_url: str | None
    user_id: int
    industry_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreateEnterpriseDTO(ORJSONModel):
    name: str = Field(..., min_length=3, max_length=100, description="The enterprise name (3 to 100 characters).")
    description: str | None = Field(None, max_length=5000,
                                    description="The enterprise description (max 5000 characters).")
    website_url: str | None = Field(None, max_length=500,
                                    description="The enterprise website URL (max 500 characters).")
    logo_url: str | None = Field(None, max_length=500, description="The enterprise logo URL (max 500 characters).")
    industry_id: int = Field(..., ge=1, description="The ID of the industry the enterprise belongs to.")

    def to_entity(self):
        from app.configs.db.database import EnterpriseEntity
        return EnterpriseEntity(**self.model_dump(exclude_none=True))

class UpdateEnterpriseDTO(ORJSONModel):
    name: str | None = Field(None, min_length=3, max_length=100,
                             description="The enterprise name (3 to 100 characters).")
    description: str | None = Field(None, max_length=5000,
                                    description="The enterprise description (max 5000 characters).")
    website_url: str | None = Field(None, max_length=500,
                                    description="The enterprise website URL (max 500 characters).")
    logo_url: str | None = Field(None, max_length=500, description="The enterprise logo URL (max 500 characters).")
    industry_id: int | None = Field(None, ge=1, description="The ID of the industry the enterprise belongs to.")