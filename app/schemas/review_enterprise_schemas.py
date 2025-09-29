from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum
from app.configs.db.database import ReviewEnterprise

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

class UpdateReviewEnterpriseDTO(ORJSONModel):
    rating: int | None
    title: str | None
    description: str | None
    pros: str | None
    cons: str | None
    would_recommend: bool | None
    position: str | None
    salary_range: str | None
    employment_type: EmploymentTypeEnum | None
    employment_status: EmploymentStatusEnum | None
    enterprise_id: int | None

class CreateReviewEnterpriseDTO(ORJSONModel):
    rating: int
    title: str
    description: str
    pros: str | None
    cons: str | None
    would_recommend: bool
    position: str | None
    salary_range: str | None
    employment_type: EmploymentTypeEnum
    employment_status: EmploymentStatusEnum
    enterprise_id: int

    def to_entity(self):
        from app.configs.db.database import ReviewEnterprise

        return ReviewEnterprise(
            rating = self.rating,
            title = self.title,
            description = self.description,
            pros = self.pros,
            cons = self.cons,
            would_recommend = self.would_recommend,
            position = self.position,
            salary_range = self.salary_range,
            employment_type = self.employment_type,
            employment_status = self.employment_status,
            enterprise_id = self.enterprise_id,
        )