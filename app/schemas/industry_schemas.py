from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel

class IndustryOUT(ORJSONModel):
    id: int
    name: str
    description: str | None
    icon_url: str | None
    is_active: bool
    usage_count: int
    user_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreateIndustryDTO(ORJSONModel):
    name: str = Field(..., min_length=3, max_length=100, description="The industry name (3 to 100 characters).")
    description: str | None = Field(None, max_length=2000, description="A description of the industry (max 2000 characters).")
    icon_url: str | None = Field(None, max_length=255, description="URL of the industry icon (max 255 characters).")

    def to_entity(self):
        from app.configs.db.database import IndustryEntity
        return IndustryEntity(**self.model_dump(exclude_none=True))

class UpdateIndustryDTO(ORJSONModel):
    name: str | None = Field(None, min_length=3, max_length=100, description="The industry name (3 to 100 characters).")
    description: str | None = Field(None, max_length=2000, description="A description of the industry (max 2000 characters).")
    icon_url: str | None = Field(None, max_length=255, description="URL of the industry icon (max 255 characters).")
    is_active: bool | None = Field(None, description="Sets whether the industry is active/available.")