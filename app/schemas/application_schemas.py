from datetime import datetime

from pydantic import Field

from app.configs.db.enums import ApplicationStatusEnum, ApplicationSourceEnum
from app.configs.orjson.orjson_config import ORJSONModel


class ApplicationOUT(ORJSONModel):
    id: int
    user_id: int
    vacancy_id: int
    status: ApplicationStatusEnum
    is_viewed: bool
    priority_level: int | None
    rating: int | None
    feedback: str | None
    source: ApplicationSourceEnum | None
    notes: str | None
    applied_at: datetime
    updated_at: datetime

class UpdateApplicationDTO(ORJSONModel):
    status: ApplicationStatusEnum | None = Field(None, description="Status of the application")
    is_viewed: bool | None = Field(None, description="Whether the application has been viewed")
    priority_level: int | None = Field(None, ge=1, le=5, description="Priority level (1-5)")
    rating: int | None = Field(None, ge=1, le=10, description="Rating given to the application (1-10)")
    feedback: str | None = Field(None, max_length=1000, description="Feedback message (up to 1000 chars)")
    source: ApplicationSourceEnum | None = Field(None, description="Origin of the application")
    notes: str | None = Field(None, max_length=2000, description="Internal notes about the application")