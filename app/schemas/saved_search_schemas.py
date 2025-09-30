from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime
from app.configs.db.database import SavedSearchEntity

class SavedSearchOUT(ORJSONModel):
    id: int
    user_id: int
    name: str
    query: dict
    description: str | None
    is_public: bool
    last_executed_at: datetime | str | None
    execution_count: int
    notifications_enabled: bool
    created_at: datetime | str
    updated_at: datetime | str

class CreateSavedSearchDTO(ORJSONModel):
    name: str
    query: dict
    description: str | None
    is_public: bool
    last_executed_at: datetime | None
    execution_count: int
    notifications_enabled: bool

class UpdateSavedSearchDTO(ORJSONModel):
    name: str | None
    query: dict | None
    description: str | None
    is_public: bool | None
    last_executed_at: datetime | None
    execution_count: int | None
    notifications_enabled: bool | None
