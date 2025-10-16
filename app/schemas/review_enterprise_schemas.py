from pydantic import Field

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
    rating: int | None = Field(None, ge=1, le=5,
                               description="The rating given to the enterprise (must be between 1 and 5).")
    title: str | None = Field(None, min_length=5, max_length=80, description="The review title (5 to 80 characters).")
    description: str | None = Field(None, min_length=20, max_length=5000,
                                    description="The detailed description of the review (20 to 5000 characters).")

    pros: str | None = Field(None, max_length=400,
                             description="Positive aspects of the enterprise (max 400 characters).")
    cons: str | None = Field(None, max_length=400,
                             description="Negative aspects of the enterprise (max 400 characters).")

    would_recommend: bool | None = Field(None, description="Indicates whether the user would recommend the enterprise.")

    position: str | None = Field(None, max_length=100,
                                 description="The user's position at the enterprise (max 100 characters).")
    salary_range: str | None = Field(None, max_length=100,
                                     description="The user's salary range or estimate (max 100 characters).")

    employment_type: EmploymentTypeEnum | None = Field(None, description="The type of employment.")
    employment_status: EmploymentStatusEnum | None = Field(None,
                                                           description="The status of employment (e.g., Active, Former).")

class CreateReviewEnterpriseDTO(ORJSONModel):
    rating: int = Field(..., ge=1, le=5, description="The rating given to the enterprise (must be between 1 and 5).")
    title: str = Field(..., min_length=5, max_length=80, description="The review title (5 to 80 characters).")
    description: str = Field(..., min_length=20, max_length=5000,
                             description="The detailed description of the review (20 to 5000 characters).")
    pros: str | None = Field(None, max_length=400,
                             description="Positive aspects of the enterprise (max 400 characters).")
    cons: str | None = Field(None, max_length=400,
                             description="Negative aspects of the enterprise (max 400 characters).")

    would_recommend: bool = Field(..., description="Indicates whether the user would recommend the enterprise.")
    position: str | None = Field(None, max_length=100,
                                 description="The user's position at the enterprise (max 100 characters).")
    salary_range: str | None = Field(None, max_length=100,
                                     description="The user's salary range or estimate (max 100 characters).")

    employment_type: EmploymentTypeEnum = Field(..., description="The type of employment.")
    employment_status: EmploymentStatusEnum = Field(..., description="The status of employment (e.g., Active, Former).")
    enterprise_id: int = Field(..., ge=1, description="The ID of the enterprise being reviewed.")

    def to_entity(self):
        from app.configs.db.database import ReviewEnterprise

        return ReviewEnterprise(**self.model_dump())