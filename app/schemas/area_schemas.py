from pydantic import BaseModel, Field
from datetime import datetime, date
from app.configs.orjson.orjson_config import ORJSONModel

class AreaOUT(ORJSONModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    user_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreateAreaDTO(ORJSONModel):
    name: str = Field(..., min_length=4, max_length=50, description="Name should is between range of 4 and 50")
    description: str | None = Field(None, min_length=4, max_length=400, description="description should be under of 400")
    is_active: bool = Field(True)

    def to_entity(self):
        from app.configs.db.database import AreaEntity
        return AreaEntity(**self.model_dump())

class UpdateAreaDTO(ORJSONModel):
    name: str | None = Field(None, min_length=4, max_length=50, description="Name should is between range of 4 and 50")
    description: str | None = Field(None, min_length=4, max_length=400, description="description should be under of 400")
    is_active: bool | None = Field(None)
    