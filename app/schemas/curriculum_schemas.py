from datetime import datetime
from pydantic import BaseModel

class CurriculumOUT(BaseModel):
    id: int
    user_id: int
    title: str
    is_updated: bool
    description: str | None
    created_at: datetime | str
    updated_at: datetime | str

class CreateCurriculumDTO(BaseModel):
    title: str
    description: str | None

    def to_entity(self):
        from app.configs.db.database import CurriculumEntity

        return CurriculumEntity(
            title = self.title,
            description = self.description,
        )


class UpdateCurriculumDTO(BaseModel):
    title: str | None
    is_updated: bool | None
    description: str | None