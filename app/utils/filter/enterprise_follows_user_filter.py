from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.configs.db.database import EnterpriseFollowsUserEntity

class EnterpriseFollowsUserFilter(Filter):
    followed_user__name: Optional[str] = Field(None, description="Search by followed user name (case-insensitive).")
    follower_enterprise__name: Optional[str] = Field(None, description="Search by follower enterprise name (case-insensitive).")

    class Constants(Filter.Constants):
        model = EnterpriseFollowsUserEntity