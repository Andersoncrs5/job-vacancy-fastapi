from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

class PostEnterpriseOUT(ORJSONModel):
    id: int
    title: str
    content: str
    url_image: str | None
    enterprise_id: int
    category_id: int
    created_at: datetime | str
    updated_at: datetime | str

class CreatePostEnterpriseDTO(ORJSONModel):
    title: str = Field(..., min_length=5, max_length=255, description="The post title (5 to 255 characters).")
    content: str = Field(..., min_length=10, max_length=10000,
                         description="The main content of the post (max 10,000 characters).")
    url_image: str | None = Field(None, max_length=1000,
                                  description="A URL for the post's main image (max 1000 characters).")

    def to_entity(self):
        from app.configs.db.database import PostEnterpriseEntity

        return PostEnterpriseEntity(**self.model_dump())

class UpdatePostEnterpriseDTO(ORJSONModel):
    title: str | None = Field(None, min_length=5, max_length=255, description="The post title (5 to 255 characters).")
    content: str | None = Field(None, max_length=10000,
                                description="The main content of the post (max 10,000 characters).")
    url_image: str | None = Field(None, max_length=1000,
                                  description="A URL for the post's main image (max 1000 characters).")