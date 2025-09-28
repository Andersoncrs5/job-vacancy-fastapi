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
    user_id: int 
    position: str | None 
    salary_range: str | None 
    employment_type: EmploymentTypeEnum 
    employment_status: EmploymentStatusEnum 
    start_date: date

    def to_entity(self):
        from app.configs.db.database import EmployeeEnterpriseEntity

        return EmployeeEnterpriseEntity(
            position = self.position,
            salary_range = self.salary_range,
            employment_type = self.employment_type,
            employment_status = self.employment_status,
            start_date = self.start_date,
        )

class UpdateEmployeeEnterpriseDTO(ORJSONModel):
    position: str | None 
    salary_range: str | None 
    employment_type: EmploymentTypeEnum | None
    employment_status: EmploymentStatusEnum | None
    start_date: date | None
    end_date: date | None
    