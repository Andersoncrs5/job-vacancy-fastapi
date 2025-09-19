from pydantic import BaseModel

class CreateCategoryDTO(BaseModel):
    name: str
    slug: str
    description: str | None
    order: int
    icon_url: str | None

    def to_category_entity(self):
        from app.configs.db.database import CategoryEntity

        return CategoryEntity(
            name = self.name,
            slug = self.slug,
            description = self.description,
            order = self.order,
            icon_url = self.icon_url,
        )


class UpdateCategoryDTO(BaseModel):
    name: str | None
    slug: str | None
    description: str | None
    order: int | None
    icon_url: str | None