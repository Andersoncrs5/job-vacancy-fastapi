from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

class SkillOUT(ORJSONModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime | str
    updated_at: datetime | str 

class CreateSkillDTO(ORJSONModel):
    name: str

    def to_entity(self):
        from app.configs.db.database import SkillEntity
        
        return SkillEntity(
            name = self.name
        )

class UpdateSkillDTO(ORJSONModel):
    name: str | None
    is_active: bool | None