from datetime import datetime
from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class CurriculumOUT(BaseSchemas):
    id: int
    user_id: int
    title: str
    is_updated: bool
    is_visible: bool
    description: str | None

class CreateCurriculumDTO(ORJSONModel):
    title: str = Field(..., min_length=5, max_length=200, description="The curriculum title (5 to 200 characters).")
    description: str | None = Field(None, max_length=5000,
                                    description="The curriculum description or summary (max 5000 characters).")

    def to_entity(self):
        from app.configs.db.database import CurriculumEntity
        return CurriculumEntity(**self.model_dump(exclude_none=True))

class UpdateCurriculumDTO(ORJSONModel):
    title: str | None = Field(None, min_length=5, max_length=200,
                              description="The curriculum title (5 to 200 characters).")
    is_updated: bool | None = Field(None, description="Indicates if the curriculum content has been updated.")
    is_visible: bool | None = Field(None, description="Sets whether the curriculum is visible to others.")
    description: str | None = Field(None, max_length=5000,
                                    description="The curriculum description or summary (max 5000 characters).")