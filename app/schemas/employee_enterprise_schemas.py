from pydantic import BaseModel
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
    enterprise_id: int 
    position: str | None 
    salary_range: str | None 
    employment_type: EmploymentTypeEnum 
    employment_status: EmploymentStatusEnum 
    start_date: date
    end_date: date | None

class UpdateEmployeeEnterpriseDTO(ORJSONModel):
    position: str | None 
    salary_range: str | None 
    employment_type: EmploymentTypeEnum | None
    employment_status: EmploymentStatusEnum | None
    start_date: date | None
    end_date: date | None
    