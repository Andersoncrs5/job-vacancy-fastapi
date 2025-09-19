from pydantic import BaseModel

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