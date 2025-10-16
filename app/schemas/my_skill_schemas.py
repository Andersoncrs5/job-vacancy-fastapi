from pydantic import Field
from pydantic.v1 import validator

from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime, date
from app.configs.db.enums import ProficiencyEnum

class MySkillOUT(ORJSONModel):
    user_id: int
    skill_id: int
    proficiency: ProficiencyEnum
    certificate_url: str | None
    datails: str | None
    years_of_experience: int | None
    last_used_date: date | str
    created_at: datetime | str
    updated_at: datetime | str

class UpdateMySkillDTO(ORJSONModel):
    proficiency: ProficiencyEnum | None = Field(None, description="The updated proficiency level in the skill.")
    certificate_url: str | None = Field(None, max_length=500,
                                        description="URL to a certificate or proof of competence (max 500 characters).")
    datails: str | None = Field(None, max_length=2000,
                                description="Additional details or context about the skill experience (max 2000 characters).")
    years_of_experience: int | None = Field(None, ge=0,
                                            description="Years of experience with this skill (must be non-negative).")
    last_used_date: date | None = Field(None, description="The date the skill was last actively used.")

    @validator('*', pre=True, always=True)
    def check_at_least_one_field(cls, value, field):
        return value

class CreateMySkillDTO(ORJSONModel):
    skill_id: int = Field(..., ge=1, description="The ID of the skill being added to the user's profile.")
    proficiency: ProficiencyEnum = Field(..., description="The user's proficiency level in the skill.")
    certificate_url: str | None = Field(None, max_length=500,
                                        description="URL to a certificate or proof of competence (max 500 characters).")
    datails: str | None = Field(None, max_length=2000, description="Additional details or context about the skill experience (max 2000 characters).")
    years_of_experience: int | None = Field(None, ge=0, description="Years of experience with this skill (must be non-negative).")
    last_used_date: date = Field(..., description="The date the skill was last actively used.")

    def to_entity(self):
        from app.configs.db.database import MySkillEntity

        return MySkillEntity(**self.model_dump(exclude_none=True))