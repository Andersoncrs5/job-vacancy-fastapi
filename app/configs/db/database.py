import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Final
from sqlalchemy import DateTime, String, func, Text, ForeignKey, Boolean, Integer
from datetime import datetime

load_dotenv()

DATABASE_URL: Final[str | None] = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is None")

engine: Final[AsyncEngine] = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    posts: Mapped[list["PostUserEntity"]] = relationship("PostUserEntity", back_populates="owner")
    categories: Mapped[list["CategoryEntity"]] = relationship("CategoryEntity", back_populates="owner")
    industries: Mapped[list["IndustryEntity"]] = relationship("IndustryEntity", back_populates="owner")

    def to_user_out(self):
        from app.schemas.user_schemas import UserOUT

        return UserOUT(
            id = self.id,
            name = self.name,
            email = self.email,
        )

class IndustryEntity(Base):
    __tablename__ = "industries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    usage_count: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="industries")

# class EnterpriseEntity(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), nullable=False)

#     description: Mapped[str | None] = mapped_column(Text, nullable=True)
#     website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
#     logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class CategoryEntity(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    post_count: Mapped[int] = mapped_column(Integer, default=0)
    job_count: Mapped[int] = mapped_column(Integer, default=0)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    children: Mapped[list["CategoryEntity"]] = relationship("CategoryEntity", backref="parent", remote_side="CategoryEntity.id")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="categories")
    posts: Mapped[list["PostUserEntity"]] = relationship("PostUserEntity", back_populates="category")

    def to_category_out(self):
        from app.schemas.category_schemas import CategoryOUT

        return CategoryOUT(
            id = self.id,
            name = self.name,
            slug = self.slug,
            description = self.description,
            is_active = self.is_active,
            order = self.order,
            post_count = self.post_count,
            job_count = self.job_count,
            icon_url = self.icon_url,
            user_id = self.user_id,
            parent_id = self.parent_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class PostUserEntity(Base):
    __tablename__ = "posts_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url_image: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="posts")
    category: Mapped["CategoryEntity"] = relationship("CategoryEntity", back_populates="posts")

    def to_out(self):
        from app.schemas.post_user_schemas import PostUserOUT

        return PostUserOUT(
            id = self.id,
            title = self.title,
            content = self.content,
            url_image = self.url_image,
            user_id = self.user_id,
            category_id = self.category_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )