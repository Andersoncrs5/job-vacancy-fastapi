from pydantic import BaseModel

class CreateCategoryDTO(BaseModel):
    name: str
    slug: str
    description: str | None
    order: int
    icon_url: str | None

class UpdateCategoryDTO(BaseModel):
    name: str | None
    slug: str | None
    description: str | None
    order: int | None
    icon_url: str | None