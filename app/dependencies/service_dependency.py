from aiokafka import AIOKafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Final
from app.configs.db.database import get_db
from app.repositories.providers.application_repository_provider import ApplicationRepositoryProvider
from app.repositories.providers.comment_post_enterprise_repository_provider import \
    CommentPostEnterpriseRepositoryProvider
from app.repositories.providers.comment_post_user_repository_provider import CommentPostUserRepositoryProvider
from app.repositories.providers.enterprise_follows_user_repository_provider import \
    EnterpriseFollowsUserRepositoryProvider
from app.repositories.providers.enterprise_metric_repository_provider import EnterpriseMetricRepositoryProvider
from app.repositories.providers.favorite_comment_post_enterprise_repository_provider import \
    FavoriteCommentPostEnterpriseRepositoryProvider
from app.repositories.providers.favorite_comment_post_user_repository_provider import \
    FavoriteCommentPostUserRepositoryProvider
from app.repositories.providers.follow_enterprise_repository_provider import FollowEnterpriseRepositoryProvider
from app.repositories.providers.follow_repository_provider import FollowRepositoryProvider
from app.repositories.providers.post_enterprise_metric_repository_provider import PostEnterpriseMetricRepositoryProvider
from app.repositories.providers.post_user_metric_repository_provider import PostUserMetricRepositoryProvider
from app.repositories.providers.reaction_comment_post_enterprise_repository_provider import \
    ReactionCommentPostEnterpriseRepositoryProvider
from app.repositories.providers.reaction_comment_post_user_repository_provider import \
    ReactionCommentPostUserRepositoryProvider
from app.repositories.providers.reaction_post_enterprise_provider import ReactionPostEnterpriseRepositoryProvider
from app.repositories.providers.reaction_post_user_repository_provider import ReactionPostUserRepositoryProvider
from app.repositories.providers.skill_repository_provider import SkillRepositoryProvider
from app.repositories.providers.user_metric_repository_provider import UserMetricRepositoryProvider
from app.repositories.providers.vacancy_metric_repository_provider import VacancyMetricRepositoryProvider
from app.services.kafka_service import get_producer_dependency
from app.services.providers.comment_post_enterprise_service_provider import CommentPostEnterpriseServiceProvider
from app.services.providers.comment_post_user_service_provider import CommentPostUserServiceProvider
from app.services.providers.enterprise_follows_user_service_provider import EnterpriseFollowsUserServiceProvider
from app.services.providers.enterprise_metric_service_provider import EnterpriseMetricServiceProvider
from app.services.providers.favorite_comment_post_enterprise_service_provider import \
    FavoriteCommentPostEnterpriseServiceProvider
from app.services.providers.favorite_comment_post_user_service_provider import FavoriteCommentPostUserServiceProvider
from app.services.providers.post_enterprise_metric_service_provider import PostEnterpriseMetricServiceProvider
from app.services.providers.post_user_metric_service_provider import PostUserMetricServiceProvider
from app.services.providers.reaction_comment_post_enterprise_service_provider import \
    ReactionCommentPostEnterpriseServiceProvider
from app.services.providers.reaction_comment_post_user_service_provider import ReactionCommentPostUserServiceProvider
from app.services.providers.reaction_post_enterprise_service_provider import ReactionPostEnterpriseServiceProvider
from app.services.providers.reaction_post_user_service_provider import ReactionPostUserServiceProvider
from app.services.providers.application_service_provider import ApplicationServiceProvider
from app.services.providers.follow_enterprise_service_provider import FollowEnterpriseServiceProvider
from app.services.providers.follow_service_provider import FollowServiceProvider
from app.services.providers.skill_service_provider import SkillServiceProvider
from app.repositories.providers.my_skill_repository_provider import MySkillRepositoryProvider
from app.services.providers.my_skill_service_provider import MySkillServiceProvider
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.services.providers.user_metric_service_provider import UserMetricServiceProvider
from app.services.providers.user_service_provider import UserServiceProvider
from app.repositories.providers.curriculum_repository_provider import CurriculumRepositoryProvider
from app.services.providers.curriculum_service_provider import CurriculumServiceProvider
from app.repositories.providers.enterprise_repository_provider import EnterpriseRepositoryProvider
from app.services.providers.enterprise_service_provider import EnterpriseServiceProvider
from app.repositories.providers.favorite_posts_user_repository_provider import FavoritePostUserRepositoryProvider
from app.services.providers.favorite_post_user_service_provider import FavoritePostUserServiceProvider
from app.repositories.providers.media_post_user_repository_provider import MediaPostUserRepositoryProvider
from app.services.providers.media_post_user_service_provider import MediaPostUserServiceProvider
from app.repositories.providers.industry_repository_provider import IndustryRepositoryProvider
from app.services.providers.industry_service_provider import IndustryServiceProvider
from app.repositories.providers.category_repository_provider import CategoryRepositoryProvider
from app.repositories.providers.post_user_repository_provider import PostUserRepositoryProvider
from app.services.providers.category_service_provider import CategoryServiceProvider
from app.services.providers.post_user_service_provider import PostUserServiceProvider
from app.services.providers.jwt_service_provider import JwtServiceProvider
from app.services.base.jwt_service_base import JwtServiceBase
from app.repositories.providers.post_enterprise_repository_provider import PostEnterpriseRepositoryProvider
from app.services.providers.post_enterprise_service_provider import PostEnterpriseServiceProvider
from app.repositories.providers.favorite_posts_enterprise_repository_provider import FavoritePostEnterpriseRepositoryProvider
from app.services.providers.favorite_post_enterprise_service_provider import FavoritePostEnterpriseServiceProvider
from app.repositories.providers.employee_enterprise_repository_provider import EmployeeEnterpriseRepositoryProvider
from app.services.providers.employee_enterprise_service_provider import EmployeeEnterpriseServiceProvider
from app.repositories.providers.review_enterprise_repository_provider import ReviewEnterpriseRepositoryProvider
from app.services.providers.review_enterprise_service_provider import ReviewEnterpriseServiceProvider
from app.repositories.providers.saved_search_repository_provider import SavedSearchReposioryProvider
from app.services.providers.saved_search_service_provider import SavedSearchServiceProvider
from app.repositories.providers.area_repository_provider import AreaRepositoryProvider
from app.services.providers.area_service_provider import AreaServiceProvider
from app.repositories.providers.vacancy_repository_provider import VacancyRepositoryProvider
from app.services.providers.vacancy_metric_service_provider import VacancyMetricServiceProvider
from app.services.providers.vacancy_service_provider import VacancyServiceProvider
from app.repositories.providers.vacancy_skill_repository_provider import VacancySkillRepositoryProvider
from app.services.providers.vacancy_skill_service_provider import VacancySkillServiceProvider
from app.repositories.providers.address_user_repository_provider import AddressUserRepositoryProvider
from app.services.providers.address_user_service_provider import AddressUserServiceProvider
from app.repositories.providers.address_enterprise_repository_provider import AddressEnterpriseRepositoryProvider
from app.services.providers.address_enterprise_service_provider import AddressEnterpriseServiceProvider

def get_post_user_metric_service_provider_dependency(
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_producer_dependency),
) -> PostUserMetricServiceProvider:
    repository = PostUserMetricRepositoryProvider(db)
    return PostUserMetricServiceProvider(repository=repository, producer=producer)

def get_post_enterprise_metric_service_provider_dependency(
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_producer_dependency),
) -> PostEnterpriseMetricServiceProvider:
    repository = PostEnterpriseMetricRepositoryProvider(db)
    return PostEnterpriseMetricServiceProvider(repository=repository, producer=producer)

def get_enterprise_metric_service_provider_dependency(
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_producer_dependency),
) -> EnterpriseMetricServiceProvider:
    repository = EnterpriseMetricRepositoryProvider(db)
    return EnterpriseMetricServiceProvider(repository=repository, producer=producer)

def get_enterprise_follows_user_provider_dependency(db: AsyncSession = Depends(get_db)) -> EnterpriseFollowsUserServiceProvider:
    repository = EnterpriseFollowsUserRepositoryProvider(db)
    return EnterpriseFollowsUserServiceProvider(repository)

def get_vacancy_metric_service_provider_dependency(
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_producer_dependency),
) -> VacancyMetricServiceProvider:
    repository = VacancyMetricRepositoryProvider(db)
    return VacancyMetricServiceProvider(repository=repository, producer=producer)

def get_user_metric_service_provider_dependency(
        db: AsyncSession = Depends(get_db),
        producer: AIOKafkaProducer = Depends(get_producer_dependency),
) -> UserMetricServiceProvider:
    repository = UserMetricRepositoryProvider(db)
    return UserMetricServiceProvider(repository=repository, producer=producer)

def get_reaction_comment_post_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ReactionCommentPostEnterpriseServiceProvider:
    repository = ReactionCommentPostEnterpriseRepositoryProvider(db)
    return ReactionCommentPostEnterpriseServiceProvider(repository)

def get_reaction_comment_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ReactionCommentPostUserServiceProvider:
    repository = ReactionCommentPostUserRepositoryProvider(db)
    return ReactionCommentPostUserServiceProvider(repository)

def get_favorite_comment_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FavoriteCommentPostUserServiceProvider:
    repository = FavoriteCommentPostUserRepositoryProvider(db)
    return FavoriteCommentPostUserServiceProvider(repository)

def get_favorite_comment_post_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FavoriteCommentPostEnterpriseServiceProvider:
    repository = FavoriteCommentPostEnterpriseRepositoryProvider(db)
    return FavoriteCommentPostEnterpriseServiceProvider(repository)

def get_comment_post_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CommentPostEnterpriseServiceProvider:
    repository = CommentPostEnterpriseRepositoryProvider(db)
    return CommentPostEnterpriseServiceProvider(repository)

def get_comment_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CommentPostUserServiceProvider:
    repository = CommentPostUserRepositoryProvider(db)
    return CommentPostUserServiceProvider(repository)

def get_reaction_post_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ReactionPostEnterpriseServiceProvider:
    repository = ReactionPostEnterpriseRepositoryProvider(db)
    return ReactionPostEnterpriseServiceProvider(repository)

def get_reaction_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ReactionPostUserServiceProvider:
    repository = ReactionPostUserRepositoryProvider(db)
    return ReactionPostUserServiceProvider(repository)

def get_follow_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FollowEnterpriseServiceProvider:
    repository: Final = FollowEnterpriseRepositoryProvider(db)
    return FollowEnterpriseServiceProvider(repository)

def get_follow_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FollowServiceProvider:
    repository: Final = FollowRepositoryProvider(db)
    return FollowServiceProvider(repository)

def get_application_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ApplicationServiceProvider:
    repository: Final = ApplicationRepositoryProvider(db)
    return ApplicationServiceProvider(repository)

def get_address_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> AddressEnterpriseServiceProvider:
    repository: Final = AddressEnterpriseRepositoryProvider(db)
    return AddressEnterpriseServiceProvider(repository)

def get_address_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> AddressUserServiceProvider:
    repository: Final = AddressUserRepositoryProvider(db)
    return AddressUserServiceProvider(repository)

def get_vacancy_skill_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> VacancySkillServiceProvider:
    repository: Final = VacancySkillRepositoryProvider(db)
    return VacancySkillServiceProvider(repository)

def get_vacancy_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> VacancyServiceProvider:
    area_repository: Final = AreaRepositoryProvider(db)
    repository: Final = VacancyRepositoryProvider(db)
    return VacancyServiceProvider(repository, area_repository)

def get_area_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> AreaServiceProvider:
    repository: Final = AreaRepositoryProvider(db)
    return AreaServiceProvider(repository)

def get_saved_search_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> SavedSearchServiceProvider:
    repository: Final = SavedSearchReposioryProvider(db)
    return SavedSearchServiceProvider(repository)

def get_review_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> ReviewEnterpriseServiceProvider:
    repository: Final = ReviewEnterpriseRepositoryProvider(db)
    return ReviewEnterpriseServiceProvider(repository)

def get_employee_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> EmployeeEnterpriseServiceProvider:
    repository: Final = EmployeeEnterpriseRepositoryProvider(db)
    return EmployeeEnterpriseServiceProvider(repository)

def get_favorite_posts_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FavoritePostEnterpriseServiceProvider:
    repository: Final = FavoritePostEnterpriseRepositoryProvider(db)
    return FavoritePostEnterpriseServiceProvider(repository)

def get_post_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> PostEnterpriseServiceProvider:
    repository: Final = PostEnterpriseRepositoryProvider(db)
    return PostEnterpriseServiceProvider(repository)

def get_my_skill_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> MySkillServiceProvider:
    repository: Final = MySkillRepositoryProvider(db)
    return MySkillServiceProvider(repository)

def get_skill_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> SkillServiceProvider:
    repository: Final = SkillRepositoryProvider(db)
    return SkillServiceProvider(repository)

def get_curriculum_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CurriculumServiceProvider:
    repository: Final = CurriculumRepositoryProvider(db)
    return CurriculumServiceProvider(repository)

def get_media_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> MediaPostUserServiceProvider:
    repository: Final = MediaPostUserRepositoryProvider(db)
    return MediaPostUserServiceProvider(repository)

def get_favorite_posts_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> FavoritePostUserServiceProvider:
    repository: Final = FavoritePostUserRepositoryProvider(db)
    return FavoritePostUserServiceProvider(repository)

def get_enterprise_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> EnterpriseServiceProvider:
    repository: Final = EnterpriseRepositoryProvider(db)
    return EnterpriseServiceProvider(repository)

def get_industry_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> IndustryServiceProvider:
    repository: Final = IndustryRepositoryProvider(db)
    return IndustryServiceProvider(repository)

def get_post_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> PostUserServiceProvider:
    repository: Final = PostUserRepositoryProvider(db)
    return PostUserServiceProvider(repository)

def get_category_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> CategoryServiceProvider:
    repository: Final = CategoryRepositoryProvider(db)
    return CategoryServiceProvider(repository)

def get_user_service_provider_dependency(db: AsyncSession = Depends(get_db)) -> UserServiceProvider:
    repository: Final = UserRepositoryProvider(db)
    return UserServiceProvider(repository)

def get_jwt_service_dependency() -> JwtServiceBase:
    return JwtServiceProvider()