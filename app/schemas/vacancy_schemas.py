from app.configs.db.enums import (
    EmploymentTypeEnum, ExperienceLevelEnum, EducationLevelEnum, 
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum
)
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel

class VacancyOUT(ORJSONModel):
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
    views_count: int
    applications_count: int
    last_application_at: datetime | str | None
    created_at: datetime | str
    updated_at: datetime | str

class CreateVacancyDTO(ORJSONModel):
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
    application_deadline: datetime | None

    def to_entity(self):
        from app.configs.db.database import VacancyEntity

        return VacancyEntity(
            area_id = self.area_id,
            title = self.title,
            description = self.description,
            employment_type = self.employment_type,
            experience_level = self.experience_level,
            education_level = self.education_level,
            workplace_type = self.workplace_type,
            seniority = self.seniority,
            salary_min = self.salary_min,
            salary_max = self.salary_max,
            currency = self.currency,
            requirements = self.currency,
            responsibilities = self.responsibilities,
            benefits = self.benefits,
            status = self.status,
            openings = self.openings,
            application_deadline = self.application_deadline,
        )
    

class UpdateVacancyDTO(ORJSONModel):
    area_id: int | None
    title: str | None
    description: str | None
    employment_type: EmploymentTypeEnum | None
    experience_level: ExperienceLevelEnum | None
    education_level: EducationLevelEnum | None
    workplace_type: WorkplaceTypeEnum | None
    seniority: int | None
    salary_min: float | None
    salary_max: float | None
    currency: str | None
    requirements: str | None
    responsibilities: str | None
    benefits: str | None
    status: VacancyStatusEnum | None
    openings: int | None
    application_deadline: datetime | None