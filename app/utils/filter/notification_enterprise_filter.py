from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import NotificationEnterpriseEntity
from app.configs.db.enums import NotificationTypeEnum


class NotificationEnterpriseFilter(Filter):
    enterprise_id: Optional[int] = Field(None, description="Filter by enterprise ID.")
    entity_id: Optional[int] = Field(None, description="Filter by related entity ID (e.g., Post ID, Comment ID).")
    type: Optional[NotificationTypeEnum] = Field(None, description="Filter by notification type.")
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")

    class Constants(Filter.Constants):
        model = NotificationEnterpriseEntity