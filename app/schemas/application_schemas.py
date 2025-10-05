from datetime import datetime

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
    status: ApplicationStatusEnum | None
    is_viewed: bool | None
    priority_level: int | None
    rating: int | None
    feedback: str | None
    source: ApplicationSourceEnum | None
    notes: str | None