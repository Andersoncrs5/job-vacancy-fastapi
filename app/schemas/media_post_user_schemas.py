from datetime import datetime

from pydantic import Field

from app.configs.db.enums import MediaType
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import BaseSchemas


class MediaPostUserOUT(BaseSchemas):
    id: int 
    url: str 
    type: MediaType 
    order: int 
    caption: str | None 
    size: int | None 
    mime_type: str | None 
    post_id: int

class CreateMediaPostUserDTO(ORJSONModel):
    url: str = Field(..., min_length=5, max_length=800, description="The URL of the media file (max 800 characters).")
    type: MediaType = Field(..., description="The type of media (e.g., image, video, gif).")
    order: int = Field(0, ge=0, description="The display order of the media within the post (must be non-negative).")
    caption: str | None = Field(None, max_length=255, description="A short caption for the media (max 255 characters).")
    size: int | None = Field(None, ge=1, description="The size of the media file in bytes (must be positive).")
    mime_type: str | None = Field(None, max_length=100, description="The MIME type of the file (max 100 characters).")

    def to_entity(self):
        from app.configs.db.database import MediaPostUserEntity

        return MediaPostUserEntity(**self.model_dump(exclude_none=True))

class UpdateMediaPostUserDTO(ORJSONModel):
    url: str | None = Field(None, min_length=5, max_length=800, description="The URL of the media file (max 800 characters).")
    type: MediaType | None = Field(None, description="The type of media (e.g., image, video, gif).")
    order: int | None = Field(None, ge=0, description="The display order of the media within the post (must be non-negative).")
    caption: str | None = Field(None, max_length=255, description="A short caption for the media (max 255 characters).")
    size: int | None = Field(None, ge=1, description="The size of the media file in bytes (must be positive).")
    mime_type: str | None = Field(None, max_length=100, description="The MIME type of the file (max 100 characters).")