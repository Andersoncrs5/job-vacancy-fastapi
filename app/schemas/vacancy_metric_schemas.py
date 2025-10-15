from datetime import datetime

from app.configs.orjson.orjson_config import ORJSONModel


class VacancyMetricOUT(ORJSONModel):
    vacancy_id: int
    shortlists_count: int
    shares_count: int
    views_count: int
    applications_count: int
    interview_count: int
    created_at: datetime
    updated_at: datetime