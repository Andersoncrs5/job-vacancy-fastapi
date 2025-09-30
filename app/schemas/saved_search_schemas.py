from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

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

    def to_entity(self):
        from app.configs.db.database import SavedSearchEntity

        return SavedSearchEntity(
            name = self.name,
            query = self.query,
            description = self.description,
            is_public = self.is_public,
            last_executed_at = self.last_executed_at,
            execution_count = self.execution_count,
            notifications_enabled = self.notifications_enabled,
        )

class UpdateSavedSearchDTO(ORJSONModel):
    name: str | None
    query: dict | None
    description: str | None
    is_public: bool | None
    last_executed_at: datetime | None
    notifications_enabled: bool | None
