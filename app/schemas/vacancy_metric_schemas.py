from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class VacancyMetricOUT(BaseSchemas):
    vacancy_id: int
    shortlists_count: int
    shares_count: int
    views_count: int
    applications_count: int
    interview_count: int