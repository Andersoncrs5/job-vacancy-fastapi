from pydantic import BaseModel
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

class UpdateIndustryDTO(ORJSONModel):
    name: str | None
    description: str | None
    icon_url: str | None
    is_active: bool | None
