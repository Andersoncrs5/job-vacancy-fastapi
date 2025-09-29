from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum

class ReviewEnterpriseOUT(ORJSONModel):
    id: int
    rating: int
    title: str
    description: str | None
    pros: str | None
    cons: str | None
    would_recommend: bool
    position: str | None
    salary_range: str | None
    employment_type: EmploymentTypeEnum
    employment_status: EmploymentStatusEnum
    helpful_votes: int
    unhelpful_votes: int
    user_id: int
    enterprise_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreateReviewEnterpriseDTO(ORJSONModel):
    rating: int
    title: str
    description: str | None
    pros: str | None
    cons: str | None
    would_recommend: bool
    position: str | None
    salary_range: str | None
    employment_type: EmploymentTypeEnum
    employment_status: EmploymentStatusEnum
    enterprise_id: int