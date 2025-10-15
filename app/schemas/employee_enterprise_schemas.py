from pydantic import BaseModel, Field
from datetime import datetime, date
from app.configs.orjson.orjson_config import ORJSONModel
from app.configs.db.enums import EmploymentTypeEnum, EmploymentStatusEnum

class EmployeeEnterpriseOUT(ORJSONModel):
    id: int
    user_id: int 
    enterprise_id: int 
    position: str | None 
    salary_range: str | None 
    employment_type: EmploymentTypeEnum 
    employment_status: EmploymentStatusEnum 
    start_date: date | None | str
    end_date: date | None | str
    created_at: datetime | str
    updated_at: datetime | str

class CreateEmployeeEnterpriseDTO(ORJSONModel):
    user_id: int = Field(..., ge=1, description="The ID of the user being hired.")
    position: str | None = Field(None, max_length=150,
                                 description="The employee's official position (max 150 characters).")
    salary_range: str | None = Field(None, max_length=100,
                                     description="The salary range for the position (max 100 characters).")
    employment_type: EmploymentTypeEnum = Field(..., description="The type of employment (e.g., Full-time, Part-time).")
    employment_status: EmploymentStatusEnum = Field(...,
                                                    description="The current status of the employment (e.g., Active, Probation).")
    start_date: date = Field(..., description="The official start date of employment.")

    def to_entity(self):
        from app.configs.db.database import EmployeeEnterpriseEntity
        return EmployeeEnterpriseEntity(**self.model_dump(exclude_none=True))

class UpdateEmployeeEnterpriseDTO(ORJSONModel):
    position: str | None = Field(None, max_length=150,
                                 description="The employee's official position (max 150 characters).")
    salary_range: str | None = Field(None, max_length=100,
                                     description="The salary range for the position (max 100 characters).")
    employment_type: EmploymentTypeEnum | None = Field(None, description="The updated type of employment.")
    employment_status: EmploymentStatusEnum | None = Field(None, description="The updated status of the employment.")
    start_date: date | None = Field(None, description="The updated official start date of employment.")
    end_date: date | None = Field(None,
                                  description="The end date of employment (used when terminating or transferring).")