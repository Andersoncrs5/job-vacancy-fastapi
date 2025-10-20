from datetime import datetime
from typing import Final

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import NotificationEnterpriseEntity
from app.repositories.base.notification_enterprise_repository_base import NotificationEnterpriseRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.notification_enterprise_filter import NotificationEnterpriseFilter


class NotificationEnterpriseRepositoryProvider(
    NotificationEnterpriseRepositoryBase,
    GenericRepository[
        NotificationEnterpriseEntity,
        NotificationEnterpriseFilter,
        int,
        NotificationEnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=NotificationEnterpriseEntity)