from datetime import datetime
from pydantic import BaseModel
from app.configs.db.enums import MediaType

class MediaPostUserOUT(BaseModel):
    id: int 
    url: str 
    type: MediaType 
    order: int 
    caption: str | None 
    size: int | None 
    mime_type: str | None 
    post_id: int 
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True

class CreateMediaPostUserDTO(BaseModel):
    url: str
    type: MediaType
    order: int
    caption: str | None
    size: int | None
    mime_type: str | None

    def to_entity(self):
        from app.configs.db.database import MediaPostUserEntity

        return MediaPostUserEntity(
            url = self.url,
            type = self.type,
            order = self.order,
            caption = self.caption,
            size = self.size,
            mime_type = self.mime_type,
        )

class UpdateMediaPostUserDTO(BaseModel):
    url: str | None
    type: MediaType | None
    order: int | None
    caption: str | None
    size: int | None
    mime_type: str | None