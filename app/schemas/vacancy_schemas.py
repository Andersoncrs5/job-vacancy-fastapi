from pydantic import Field

from app.configs.db.enums import (
    EmploymentTypeEnum, ExperienceLevelEnum, EducationLevelEnum, 
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum
)
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class VacancyOUT(BaseSchemas):
    id: int
    enterprise_id: int
    area_id: int
    title: str
    description: str
    employment_type: EmploymentTypeEnum
    experience_level: ExperienceLevelEnum
    education_level: EducationLevelEnum | None
    workplace_type: WorkplaceTypeEnum
    seniority: int | None
    salary_min: float | None
    salary_max: float | None
    currency: str | None
    requirements: str | None
    responsibilities: str | None
    benefits: str | None
    status: VacancyStatusEnum
    openings: int
    application_deadline: datetime | str | None
    last_application_at: datetime | str | None

class CreateVacancyDTO(ORJSONModel):
    area_id: int = Field(..., ge=1, description="The ID of the functional area the vacancy belongs to.")
    title: str = Field(..., min_length=5, max_length=250, description="The job title (5 to 250 characters).")
    description: str = Field(..., min_length=50, max_length=15000,
                             description="The detailed job description (50 to 15,000 characters).")
    employment_type: EmploymentTypeEnum = Field(..., description="The type of employment (e.g., Full-time, Part-time).")
    experience_level: ExperienceLevelEnum = Field(..., description="The required level of experience.")
    education_level: EducationLevelEnum | None = Field(None, description="The minimum required education level.")
    workplace_type: WorkplaceTypeEnum = Field(..., description="The type of workplace (e.g., Onsite, Remote).")
    seniority: int | None = Field(None, ge=0, description="Seniority in years (must be non-negative).")

    salary_min: float | None = Field(None, ge=0.0, description="The minimum salary offered (must be non-negative).")
    salary_max: float | None = Field(None, ge=0.0, description="The maximum salary offered (must be non-negative).")
    currency: str | None = Field(None, max_length=10,
                                 description="The currency code for the salary (max 10 characters).")
    requirements: str | None = Field(None, max_length=300,
                                     description="Key requirements for the role (max 300 characters).")
    responsibilities: str | None = Field(None, max_length=300,
                                         description="Key responsibilities for the role (max 300 characters).")
    benefits: str | None = Field(None, max_length=300, description="Benefits offered (max 300 characters).")
    status: VacancyStatusEnum = Field(VacancyStatusEnum.OPEN, description="The current status of the vacancy.")
    openings: int = Field(1, ge=1, description="The number of positions available (must be at least 1).")
    application_deadline: datetime | None = Field(None, description="The deadline for applications.")

    def to_entity(self):
        from app.configs.db.database import VacancyEntity

        return VacancyEntity(**self.model_dump(exclude_none=True))

class UpdateVacancyDTO(ORJSONModel):
    area_id: int | None = Field(None, ge=1, description="The ID of the functional area the vacancy belongs to.")
    title: str | None = Field(None, min_length=5, max_length=250, description="The job title (5 to 250 characters).")
    description: str | None = Field(None, min_length=50, max_length=15000,
                                    description="The detailed job description (50 to 15,000 characters).")

    employment_type: EmploymentTypeEnum | None = Field(None, description="The type of employment.")
    experience_level: ExperienceLevelEnum | None = Field(None, description="The required level of experience.")
    education_level: EducationLevelEnum | None = Field(None, description="The minimum required education level.")
    workplace_type: WorkplaceTypeEnum | None = Field(None, description="The type of workplace.")

    seniority: int | None = Field(None, ge=0, description="Seniority in years (must be non-negative).")

    salary_min: float | None = Field(None, ge=0.0, description="The minimum salary offered (must be non-negative).")
    salary_max: float | None = Field(None, ge=0.0, description="The maximum salary offered (must be non-negative).")
    currency: str | None = Field(None, max_length=10,
                                 description="The currency code for the salary (max 10 characters).")

    requirements: str | None = Field(None, max_length=300,
                                     description="Key requirements for the role (max 300 characters).")
    responsibilities: str | None = Field(None, max_length=300,
                                         description="Key responsibilities for the role (max 300 characters).")
    benefits: str | None = Field(None, max_length=300, description="Benefits offered (max 300 characters).")

    status: VacancyStatusEnum | None = Field(None, description="The current status of the vacancy.")
    openings: int | None = Field(None, ge=1, description="The number of positions available (must be at least 1).")
    application_deadline: datetime | None = Field(None, description="The deadline for applications.")