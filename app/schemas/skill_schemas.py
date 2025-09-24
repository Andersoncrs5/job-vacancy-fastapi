from app.configs.orjson.orjson_config import ORJSONModel
from uuid import UUID
from datetime import datetime

class SkillEntity(ORJSONModel):
    id: UUID
    name: str
    is_active: bool
    refresh_token: str
    created_at: datetime | str
    updated_at: datetime | str 

class CreateSkillDTO(ORJSONModel):
    name: str

class UpdateSkillDTO(ORJSONModel):
    name: str | None
    is_active: bool | None