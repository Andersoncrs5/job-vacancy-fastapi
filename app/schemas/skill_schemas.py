from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

class SkillOUT(ORJSONModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime | str
    updated_at: datetime | str 

class CreateSkillDTO(ORJSONModel):
    name: str = Field(..., min_length=3, max_length=100, description="The name of the skill (3 to 100 characters).")

    def to_entity(self):
        from app.configs.db.database import SkillEntity
        
        return SkillEntity(**self.model_dump(exclude_none=True))

class UpdateSkillDTO(ORJSONModel):
    name: str | None = Field(None, min_length=3, max_length=100,
                             description="The updated name of the skill (3 to 100 characters).")
    is_active: bool | None = Field(None, description="Sets whether the skill is active and available for use.")