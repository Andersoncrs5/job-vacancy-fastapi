from datetime import datetime
from typing import Final

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db.database import NotificationEntity
from app.repositories.base.notification_repository_base import NotificationRepositoryBase
from app.repositories.generics.generic_repository import GenericRepository
from app.utils.filter.notification_filter import NotificationFilter


class NotificationRepositoryProvider(
    NotificationRepositoryBase,
    GenericRepository[
        NotificationEntity,
        NotificationFilter,
        int,
        NotificationEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=NotificationEntity)