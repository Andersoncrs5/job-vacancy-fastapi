import os
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Final
from sqlalchemy import DateTime, String, func, Text, ForeignKey, Boolean, Integer, BigInteger, Enum
from datetime import datetime, date
from sqlalchemy.pool import NullPool
from app.configs.db.enums import MediaType, ProficiencyEnum
import uuid

load_dotenv()

DATABASE_URL: Final[str | None] = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is None")

engine: Final[AsyncEngine] = create_async_engine(DATABASE_URL, future=True, echo=True, poolclass=NullPool)

AsyncSessionLocal: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    posts: Mapped[list["PostUserEntity"]] = relationship("PostUserEntity", back_populates="owner")
    categories: Mapped[list["CategoryEntity"]] = relationship("CategoryEntity", back_populates="owner")
    industries: Mapped[list["IndustryEntity"]] = relationship("IndustryEntity", back_populates="owner")

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="owner", uselist=False)
    curriculum: Mapped["CurriculumEntity"] = relationship("CurriculumEntity", back_populates="owner", uselist=False)

    favorite_post_user: Mapped[list["FavoritePostUserEntity"]] = relationship("FavoritePostUserEntity", back_populates="owner")
    my_skills: Mapped[list["MySkillEntity"]] = relationship("MySkillEntity", back_populates="owner")

    def to_user_out(self):
        from app.schemas.user_schemas import UserOUT

        return UserOUT(
            id = self.id,
            name = self.name,
            email = self.email,
            avatar_url = self.avatar_url,
            created_at = str(self.created_at),
            bio = self.bio,
        )

class MySkillEntity(Base):
    __tablename__ = "my_skills"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True,
        nullable=False
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), 
        primary_key=True,
        nullable=False
    )

    proficiency: Mapped[ProficiencyEnum] = mapped_column(
        Enum(ProficiencyEnum), 
        default=ProficiencyEnum.basic, 
        nullable=False
    )
    
    certificate_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    datails: Mapped[str | None] = mapped_column(Text, nullable=True)

    years_of_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    last_used_date: Mapped[date] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="my_skills")
    
    skill: Mapped["SkillEntity"] = relationship("SkillEntity", back_populates="my_skills")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_out(self):
        from app.schemas.my_skill_schemas import MySkillOUT

        return MySkillOUT(
            skill_id = self.skill_id,
            user_id = self.user_id,
            proficiency = self.proficiency,
            certificate_url = self.certificate_url,
            datails = self.datails,
            years_of_experience = self.years_of_experience,
            last_used_date = str(self.last_used_date),
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class SkillEntity(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    my_skills: Mapped[list["MySkillEntity"]] = relationship("MySkillEntity", back_populates="skill")

    def to_out(self):
        from app.schemas.skill_schemas import SkillOUT

        return SkillOUT(
            id = self.id,
            name = self.name,
            is_active = self.is_active,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class CurriculumEntity(Base):
    __tablename__ = "curriculums"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    is_updated: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="curriculum")

    def to_out(self):
        from app.schemas.curriculum_schemas import CurriculumOUT

        return CurriculumOUT(
            id = self.id,
            user_id = self.user_id,
            title = self.title,
            is_updated = self.is_updated,
            description = self.description,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class IndustryEntity(Base):
    __tablename__ = "industries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    usage_count: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="industries")
    
    enterprises: Mapped[list["EnterpriseEntity"]] = relationship(
        "EnterpriseEntity", back_populates="industry"
    )

    def to_out(self):
        from app.schemas.industry_schemas import IndustryOUT

        return IndustryOUT(
            id = self.id,
            name = self.name,
            description = self.description,
            icon_url = self.icon_url,
            is_active = self.is_active,
            usage_count = self.usage_count,
            user_id = self.user_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class EnterpriseEntity(Base):
    __tablename__ = "enterprises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True)

    industry_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("industries.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="enterprise")
    industry: Mapped["IndustryEntity"] = relationship("IndustryEntity", back_populates="enterprises")

    def to_out(self):
        from app.schemas.enterprise_schemas import EnterpriseOUT

        return EnterpriseOUT(
            id = self.id,
            name = self.name,
            description = self.description,
            website_url = self.website_url,
            logo_url = self.logo_url,
            user_id = self.user_id,
            industry_id = self.industry_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class CategoryEntity(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    post_count: Mapped[int] = mapped_column(Integer, default=0)
    job_count: Mapped[int] = mapped_column(Integer, default=0)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    parent_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=True)
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url_image: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="posts")
    category: Mapped["CategoryEntity"] = relationship("CategoryEntity", back_populates="posts")

    favorite_post_user: Mapped[list["FavoritePostUserEntity"]] = relationship("FavoritePostUserEntity", back_populates="post_user")
    medias: Mapped[list["MediaPostUserEntity"]] = relationship("MediaPostUserEntity", back_populates="post")

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

class MediaPostUserEntity(Base):
    __tablename__ = "medias_post_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(800), nullable=False, index=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType, name="media_type"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0)
    caption: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_user.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    post: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="medias")

    def to_out(self):
        from app.schemas.media_post_user_schemas import MediaPostUserOUT
        return MediaPostUserOUT(
            id = self.id,
            url = self.url,
            type = self.type,
            order = self.order,
            caption = self.caption,
            size = self.size,
            mime_type = self.mime_type,
            post_id = self.post_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class FavoritePostUserEntity(Base):
    __tablename__ = "favorite_posts_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))

    post_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_user.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="favorite_post_user")
    post_user: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="favorite_post_user")
    