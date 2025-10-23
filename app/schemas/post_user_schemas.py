from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from datetime import datetime

from app.schemas.base import BaseSchemas


class PostUserOUT(BaseSchemas):
    id: int
    title: str
    content: str
    url_image: str | None
    user_id: int
    category_id: int

class CreatePostUserDTO(ORJSONModel):
    title: str = Field(..., min_length=5, max_length=255, description="The post title (5 to 255 characters).")
    content: str = Field(..., min_length=10, max_length=10000,
                         description="The main content of the post (max 10,000 characters).")
    url_image: str | None = Field(None, max_length=1000,
                                  description="A URL for the post's main image (max 1000 characters).")

    def to_entity(self):
        from app.configs.db.database import PostUserEntity

        return PostUserEntity(**self.model_dump())

class UpdatePostUserDTO(ORJSONModel):
    title: str | None = Field(None, min_length=5, max_length=255, description="The post title (5 to 255 characters).")
    content: str | None = Field(None, min_length=10, max_length=10000,
                                description="The main content of the post (max 10,000 characters).")
    url_image: str | None = Field(None, max_length=1000,
                                  description="A URL for the post's main image (max 1000 characters).")