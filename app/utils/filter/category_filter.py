from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import CategoryEntity

class CategoryFilter(Filter):
    is_active: Optional[bool] = Field(
        None,
        description="Filters by active status."
    )

    post_count__gte: Optional[int] = Field(
        None,
        description="Filters categories with a post count greater than or equal to the specified value."
    )
    job_count__gte: Optional[int] = Field(
        None,
        description="Filters categories with a job count greater than or equal to the specified value."
    )

    # Allows filtering by parent/child categories
    parent_id: Optional[int] = Field(
        None,
        description="Filters for categories that are children of the specified ID."
    )

    name__ilike: Optional[str] = Field(
        None,
        description="Search by name (case-insensitive, LIKE)."
    )

    created_at__gte: Optional[datetime] = Field(
        None,
        description="Filter by creation date, greater than or equal to."
    )

    created_at__lte: Optional[datetime] = Field(
        None,
        description="Filter by creation date, less than or equal to."
    )

    class Constants(Filter.Constants):
        model = CategoryEntity