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
    title: str
    content: str
    url_image: str | None

    def to_entity(self):
        from app.configs.db.database import PostEnterpriseEntity

        return PostEnterpriseEntity(
            title = self.title,
            content = self.content,
            url_image = self.url_image,
        )

class UpdatePostEnterpriseDTO(ORJSONModel):
    title: str | None
    content: str | None
    url_image: str | None