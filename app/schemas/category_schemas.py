from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class CategoryOUT(BaseSchemas):
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

class CreateCategoryDTO(ORJSONModel):
    name: str = Field(..., min_length=3, max_length=100, description="The category name must be between 3 and 100 characters.")
    slug: str = Field(..., min_length=3, max_length=220, description="The slug must be between 3 and 220 characters and unique.")
    description: str | None = Field(None, max_length=1000, description="The category description (max 1000 characters).")
    order: int = Field(0, ge=0, description="The category order (must be greater than or equal to 0).")
    icon_url: str | None = Field(None, max_length=500, description="URL of the category icon (max 500 characters).")
    parent_id: int | None = Field(None, description="ID of the parent category for subcategories.")

    def to_category_entity(self):
        from app.configs.db.database import CategoryEntity
        return CategoryEntity(**self.model_dump(exclude_none=True))

class UpdateCategoryDTO(ORJSONModel):
    name: str | None = Field(None, min_length=3, max_length=100, description="The category name must be between 3 and 100 characters.")
    slug: str | None = Field(None, min_length=3, max_length=220, description="The slug must be between 3 and 220 characters and unique.")
    description: str | None = Field(None, max_length=1000, description="The category description (max 1000 characters).")
    is_active: bool | None = Field(None, description="Sets whether the category is active.")
    order: int | None = Field(None, ge=0, description="The category order (must be greater than or equal to 0).")
    icon_url: str | None = Field(None, max_length=500, description="URL of the category icon (max 500 characters).")
    parent_id: int | None = Field(None, description="ID of the parent category for subcategories.")