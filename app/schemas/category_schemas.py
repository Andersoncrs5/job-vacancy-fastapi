from pydantic import BaseModel
from datetime import datetime

class CategoryOUT(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    is_active: bool
    order: int
    post_count: int
    job_count: int
    icon_url: str | None
    user_id: int
    parent_id: int | None
    created_at: datetime
    updated_at: datetime

class CreateCategoryDTO(BaseModel):
    name: str
    slug: str
    description: str | None
    order: int
    icon_url: str | None

    def to_category_entity(self):
        from app.configs.db.database import CategoryEntity

        return CategoryEntity(
            name = self.name,
            slug = self.slug,
            description = self.description,
            order = self.order,
            icon_url = self.icon_url,
        )


class UpdateCategoryDTO(BaseModel):
    name: str | None
    slug: str | None
    description: str | None
    order: int | None
    icon_url: str | None