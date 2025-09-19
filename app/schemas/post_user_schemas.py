from pydantic import BaseModel
from datetime import datetime

class PostUserOUT(BaseModel):
    id: int
    title: str
    content: str
    url_image: str | None
    user_id: int
    category_id: int
    created_at: datetime | str
    updated_at: datetime | str

    class Config:
        from_attributes = True

class CreatePostUserDTO(BaseModel):
    title: str
    content: str
    url_image: str | None

    def to_entity(self):
        from app.configs.db.database import PostUserEntity

        return PostUserEntity(
            title = self.title,
            content = self.content,
            url_image = self.url_image,
        )

class UpdatePostUserDTO(BaseModel):
    title: str | None
    content: str | None
    url_image: str | None