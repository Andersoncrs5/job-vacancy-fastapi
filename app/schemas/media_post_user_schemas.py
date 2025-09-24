from datetime import datetime
from app.configs.db.enums import MediaType
from app.configs.orjson.orjson_config import ORJSONModel

class MediaPostUserOUT(ORJSONModel):
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

class CreateMediaPostUserDTO(ORJSONModel):
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

class UpdateMediaPostUserDTO(ORJSONModel):
    url: str | None
    type: MediaType | None
    order: int | None
    caption: str | None
    size: int | None
    mime_type: str | None