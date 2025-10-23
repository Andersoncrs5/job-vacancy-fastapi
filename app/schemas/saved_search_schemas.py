from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

from app.schemas.base import BaseSchemas


class SavedSearchOUT(BaseSchemas):
    id: int
    user_id: int
    name: str
    query: dict
    description: str | None
    is_public: bool
    last_executed_at: datetime | str | None
    execution_count: int
    notifications_enabled: bool

class CreateSavedSearchDTO(ORJSONModel):
    name: str = Field(..., min_length=3, max_length=100, description="A unique name for the saved search (3 to 100 characters).")
    query: dict = Field(..., description="The criteria for the search, stored as a JSON object.")
    description: str | None = Field(None, max_length=500, description="A brief description of what the search criteria covers (max 500 characters).")
    is_public: bool = Field(False, description="Whether the saved search is visible to other users.")
    last_executed_at: datetime | None = Field(None, description="The timestamp of the last time this search was executed.")
    notifications_enabled: bool = Field(False, description="Whether the user wishes to receive notifications for new results.")

    def to_entity(self):
        from app.configs.db.database import SavedSearchEntity
        return SavedSearchEntity(**self.model_dump(exclude_none=True))

class UpdateSavedSearchDTO(ORJSONModel):
    name: str | None = Field(None, min_length=3, max_length=100, description="The updated name for the saved search (3 to 100 characters).")
    query: dict | None = Field(None, description="The updated search criteria as a JSON object.")
    description: str | None = Field(None, max_length=500, description="The updated description of the search (max 500 characters).")
    is_public: bool | None = Field(None, description="Whether the saved search is visible to other users.")
    last_executed_at: datetime | None = Field(None, description="The timestamp of the last time this search was executed.")
    notifications_enabled: bool | None = Field(None, description="Whether the user wishes to receive notifications for new results.")
