import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Final, Optional, List
from sqlalchemy import (
    DateTime, ARRAY, String, 
    func, Text, ForeignKey, 
    Boolean, Integer, BigInteger, 
    Enum, Date, JSON, Numeric
)
from datetime import datetime, date
from sqlalchemy.pool import NullPool
from app.configs.db.enums import (
    MediaType, ProficiencyEnum, EmploymentTypeEnum, 
    EmploymentStatusEnum, ExperienceLevelEnum, EducationLevelEnum, 
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum,
    AddressTypeEnum
)

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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_block: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
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

    favorite_post_enterprise: Mapped[list["FavoritePostEnterpriseEntity"]] = relationship("FavoritePostEnterpriseEntity", back_populates="owner")
    reviews: Mapped[list["ReviewEnterprise"]] = relationship("ReviewEnterprise", back_populates="owner")

    employments: Mapped[list["EmployeeEnterpriseEntity"]] = relationship("EmployeeEnterpriseEntity", back_populates="owner")
    searchs: Mapped[list["SavedSearchEntity"]] = relationship("SavedSearchEntity", back_populates="owner")

    areas: Mapped[list["AreaEntity"]] = relationship("AreaEntity", back_populates="owner")
    address: Mapped["AddressUserEntity"] = relationship("AddressUserEntity", back_populates="owner")

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

class AddressUserEntity(Base):
    __tablename__ = "addresses_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(50), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="Brasil")
    zipcode: Mapped[str] = mapped_column(String(20), nullable=True)

    address_type: Mapped[AddressTypeEnum] = mapped_column(
        Enum(AddressTypeEnum, name="address_type_enum"),
        nullable=False,
        default=AddressTypeEnum.RESIDENTIAL
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="address")

    def to_out(self):
        from app.schemas.address_user_schemas import AddressUserOUT

        return AddressUserOUT(
            id = self.id,
            user_id = self.user_id,
            street = self.street,
            number = self.number,
            complement = self.complement,
            district = self.district,
            city = self.city,
            state = self.state,
            country = self.country,
            zipcode = self.zipcode,
            address_type = self.address_type,
            is_default = self.is_default,
            created_at = self.created_at,
            updated_at = self.updated_at,
        )

class SavedSearchEntity(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True , nullable=False)
    query: Mapped[dict] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_executed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    execution_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="searchs")

    def to_out(self):
        from app.schemas.saved_search_schemas import SavedSearchOUT

        return SavedSearchOUT(
            id = self.id,
            user_id = self.user_id,
            name = self.name,
            query = self.query,
            description = self.description,
            is_public = self.is_public,
            last_executed_at = str(self.last_executed_at),
            execution_count = self.execution_count,
            notifications_enabled = self.notifications_enabled,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
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
        Enum(ProficiencyEnum, name="proficiency_enum"), 
        default=ProficiencyEnum.basic, 
        nullable=False
    )
    
    certificate_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    datails: Mapped[str | None] = mapped_column(Text, nullable=True)

    years_of_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    last_used_date: Mapped[date] = mapped_column(Date, server_default=func.now(), nullable=False)

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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    my_skills: Mapped[list["MySkillEntity"]] = relationship("MySkillEntity", back_populates="skill")
    vacancies: Mapped[List["VacancySkillEntity"]] = relationship("VacancySkillEntity", back_populates="skill")

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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
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

class AreaEntity(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="areas")

    vacancies: Mapped[list["VacancyEntity"]] = relationship(
        "VacancyEntity", 
        back_populates="area"
    )

    def to_out(self):
        from app.schemas.area_schemas import AreaOUT

        return AreaOUT(
            id = self.id,
            name = self.name,
            description = self.description,
            is_active = self.is_active,
            user_id = self.user_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class EnterpriseEntity(Base):
    __tablename__ = "enterprises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True)

    industry_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("industries.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="enterprise")
    address: Mapped["UserEntity"] = relationship("UserEntity", back_populates="enterprise")
    industry: Mapped["IndustryEntity"] = relationship("IndustryEntity", back_populates="enterprises")
    posts: Mapped[list["PostEnterpriseEntity"]] = relationship("PostEnterpriseEntity", back_populates="enterprise")
    reviews: Mapped[list["ReviewEnterprise"]] = relationship("ReviewEnterprise", back_populates="enterprise")
    employments: Mapped[list["EmployeeEnterpriseEntity"]] = relationship("EmployeeEnterpriseEntity", back_populates="enterprise")
    vacancies: Mapped[list["VacancyEntity"]] = relationship("VacancyEntity", back_populates="enterprise")

    address: Mapped["AddressEnterpriseEntity"] = relationship("AddressEnterpriseEntity", back_populates="enterprise")

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

class AddressEnterpriseEntity(Base):
    __tablename__ = "addresses_enterprise"

    enterprise_id: Mapped[int] = mapped_column(
        ForeignKey("enterprises.id"),
        nullable=False, 
        index=True,
        primary_key=True, 
    )

    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(50), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(20), nullable=True)

    address_type: Mapped[AddressTypeEnum] = mapped_column(
        Enum(AddressTypeEnum, name="address_type_enum"),
        nullable=False,
        default=AddressTypeEnum.RESIDENTIAL
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="address")

    def to_out(self):
        from app.schemas.address_enterprise_schemas import AddressEnterpriseOUT

        return AddressEnterpriseOUT(
            enterprise_id = self.enterprise_id,
            street = self.street,
            number = self.number,
            complement = self.complement,
            district = self.district,
            city = self.city,
            state = self.state,
            country = self.country,
            zipcode = self.zipcode,
            address_type = self.address_type,
            is_default = self.is_default,
            is_public = self.is_public,
            created_at = self.created_at,
            updated_at = self.updated_at,
        )

class VacancyEntity(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"), nullable=False)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), nullable=False) 

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(Enum(EmploymentTypeEnum), nullable=False)
    experience_level: Mapped[ExperienceLevelEnum] = mapped_column(Enum(ExperienceLevelEnum), nullable=False)
    education_level: Mapped[EducationLevelEnum | None] = mapped_column(Enum(EducationLevelEnum), nullable=True)

    workplace_type: Mapped[WorkplaceTypeEnum] = mapped_column(Enum(WorkplaceTypeEnum), nullable=False)

    seniority: Mapped[int | None] = mapped_column(Integer, nullable=True)

    salary_min: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)

    requirements: Mapped[str | None] = mapped_column(String(300), nullable=True)
    responsibilities: Mapped[str | None] = mapped_column(String(300), nullable=True)
    benefits: Mapped[str | None] = mapped_column(String(300), nullable=True)

    status: Mapped[VacancyStatusEnum] = mapped_column(Enum(VacancyStatusEnum), default=VacancyStatusEnum.OPEN, nullable=False)

    openings: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    application_deadline: Mapped[datetime | None] = mapped_column(Date, nullable=True)

    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    applications_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_application_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="vacancies")
    area: Mapped["AreaEntity"] = relationship("AreaEntity", back_populates="vacancies")

    skills: Mapped[List["VacancySkillEntity"]] = relationship("VacancySkillEntity", back_populates="vacancy")

    def to_out(self):
        from app.schemas.vacancy_schemas import VacancyOUT

        return VacancyOUT(
            id = self.id,
            enterprise_id = self.enterprise_id,
            area_id = self.area_id,
            title = self.title,
            description = self.description,
            employment_type = self.employment_type,
            experience_level = self.experience_level,
            education_level = self.education_level,
            workplace_type = self.workplace_type,
            seniority = self.seniority,
            salary_min = self.salary_min,
            salary_max = self.salary_max,
            currency = self.currency,
            requirements = self.requirements,
            responsibilities = self.responsibilities,
            benefits = self.benefits,
            status = self.status,
            openings = self.openings,
            application_deadline = str(self.application_deadline),
            views_count = self.views_count,
            applications_count= self.applications_count,
            last_application_at = str(self.last_application_at),
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class VacancySkillEntity(Base):
    __tablename__ = "vacancy_skills"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    proficiency: Mapped[ProficiencyEnum | None] = mapped_column(Enum(ProficiencyEnum, name="proficiency_enum"), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority_level: Mapped[int | None] = mapped_column(Integer, nullable=True)  
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    vacancy: Mapped["VacancyEntity"] = relationship("VacancyEntity", back_populates="skills")
    skill: Mapped["SkillEntity"] = relationship("SkillEntity", back_populates="vacancies")

class EmployeeEnterpriseEntity(Base):
    __tablename__ = "employees_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))

    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(EmploymentTypeEnum, name="employment_type_enum"), nullable=False
    )

    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        Enum(EmploymentStatusEnum, name="employment_status_enum"), nullable=False
    )

    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="employments")
    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="employments")

    def to_out(self):
        from app.schemas.employee_enterprise_schemas import EmployeeEnterpriseOUT

        return EmployeeEnterpriseOUT(
            id = self.id,
            user_id = self.user_id,
            enterprise_id = self.enterprise_id,
            position = self.position,
            salary_range = self.salary_range,
            employment_type = self.employment_type,
            employment_status = self.employment_status,
            start_date = str(self.start_date),
            end_date = str(self.end_date),
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )        

class ReviewEnterprise(Base):
    __tablename__ = "reviews_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    pros: Mapped[str | None] = mapped_column(String(400), nullable=True)
    cons: Mapped[str | None] = mapped_column(String(400), nullable=True)

    would_recommend: Mapped[bool] = mapped_column(Boolean, default=True)

    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(EmploymentTypeEnum, name="employment_type_enum"), nullable=False
    )

    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        Enum(EmploymentStatusEnum, name="employment_status_enum"), nullable=False
    )
    
    helpful_votes: Mapped[int] = mapped_column(Integer, default=0)
    unhelpful_votes: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="reviews")
    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="reviews")
    
    def to_out(self):
        from app.schemas.review_enterprise_schemas import ReviewEnterpriseOUT

        return ReviewEnterpriseOUT(
            id = self.id,
            rating = self.rating,
            title = self.title,
            description = self.description,
            pros = self.pros,
            cons = self.cons,
            would_recommend = self.would_recommend,
            position = self.position,
            salary_range = self.salary_range,
            employment_type = self.employment_type,
            employment_status = self.employment_status,
            helpful_votes = self.helpful_votes,
            unhelpful_votes = self.unhelpful_votes,
            user_id = self.user_id,
            enterprise_id = self.enterprise_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class PostEnterpriseEntity(Base):
    __tablename__ = "posts_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url_image: Mapped[str | None] = mapped_column(Text, nullable=True)

    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="posts")
    category: Mapped["CategoryEntity"] = relationship("CategoryEntity", back_populates="posts_enterprise")
    favorite_post_enterprise: Mapped[list["FavoritePostEnterpriseEntity"]] = relationship("FavoritePostEnterpriseEntity", back_populates="posts")

    def to_out(self):
        from app.schemas.post_enterprise_schemas import PostEnterpriseOUT

        return PostEnterpriseOUT(
            id = self.id,
            title = self.title,
            content = self.content,
            url_image = self.url_image,
            enterprise_id = self.enterprise_id,
            category_id = self.category_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )

class FavoritePostEnterpriseEntity(Base):
    __tablename__ = "favorite_posts_enterprise"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    post_enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_enterprise.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="favorite_post_enterprise")
    posts: Mapped["PostEnterpriseEntity"] = relationship("PostEnterpriseEntity", back_populates="favorite_post_enterprise")
    
class CategoryEntity(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
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
    posts_enterprise: Mapped[list["PostEnterpriseEntity"]] = relationship("PostEnterpriseEntity", back_populates="category")

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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))

    post_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_user.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="favorite_post_user")
    post_user: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="favorite_post_user")
    