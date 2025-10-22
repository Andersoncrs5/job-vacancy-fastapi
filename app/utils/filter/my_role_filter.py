from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.configs.db.database import UserRolesEntity


class MyRolesFilter(Filter):

    user_id: Optional[int] = Field(None, description="Search by ID of the associated user.")
    role_id: Optional[int] = Field(None, description="Search by ID of the associated role.")
    created_at__gte: Optional[datetime] = Field(None, description="Filter: Created on or after this datetime.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter: Created on or before this datetime.")

    class Constants(Filter.Constants):
        model = UserRolesEntity

