from datetime import datetime, UTC

from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from app.utils.enums.sum_red import SumRedEnum, ColumnUserMetricEnum
from enum import Enum

class EntityEnum(str, Enum):
    USER_METRIC = "USER_METRIC"
    VACANCY_METRIC = "VACANCY_METRIC"
    ENTERPRISE_METRIC = "ENTERPRISE_METRIC"
    POST_ENTERPRISE_METRIC = "POST_ENTERPRISE_METRIC"

class EventMessageMetric(ORJSONModel):
    event_id: str
    metric_id: int
    column: str
    action: SumRedEnum
    entity: EntityEnum
    created_at: datetime
    source: str
    metadata: dict