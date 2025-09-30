from pydantic import BaseModel
from datetime import datetime, date
from app.configs.orjson.orjson_config import ORJSONModel

class AreaOUT(ORJSONModel):
    id: int
    name: str
    description: str
    is_active: bool
    user_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreateAreaDTO(ORJSONModel):
    name: str
    description: str | None
    is_active: bool

    def to_entity(self):
        from app.configs.db.database import AreaEntity

        return AreaEntity(
            name = self.name,
            description = self.description,
            is_active = self.is_active,
        )

class UpdateAreaDTO(ORJSONModel):
    name: str | None
    description: str | None
    is_active: bool | None
    