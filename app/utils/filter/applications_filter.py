from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.configs.db.database import ApplicationEntity
from app.configs.db.enums import ApplicationStatusEnum, ApplicationSourceEnum


class ApplicationFilter(Filter):
    user_id: Optional[int] = Field(None,
                                   description="Filters by the ID of the candidate (user) who submitted the application.")
    vacancy_id: Optional[int] = Field(None, description="Filters by the ID of the vacancy the application is for.")

    status: Optional[ApplicationStatusEnum] = Field(None,
                                                    description="Filters by the current status of the application (e.g., PENDING, APPROVED, REJECTED).")
    is_viewed: Optional[bool] = Field(None,
                                      description="Filters by applications that have been viewed (True) or not viewed (False).")

    priority_level__gte: Optional[int] = Field(None,
                                               description="Filters for applications with a Priority Level greater than or equal to this value.")
    priority_level__lte: Optional[int] = Field(None,
                                               description="Filters for applications with a Priority Level less than or equal to this value.")

    rating__gte: Optional[int] = Field(None,
                                       description="Filters for applications with a Rating greater than or equal to this value.")
    rating__lte: Optional[int] = Field(None,
                                       description="Filters for applications with a Rating less than or equal to this value.")

    feedback__ilike: Optional[str] = Field(None,
                                           description="Filters (case-insensitive search) for applications where the 'feedback' field contains the provided text.")
    notes__ilike: Optional[str] = Field(None,
                                        description="Filters (case-insensitive search) for applications where the 'notes' field contains the provided text.")

    source: Optional[ApplicationSourceEnum] = Field(None,
                                                    description="Filters by the source of the application (e.g., SITE, API, MANUAL).")

    applied_at__gte: Optional[datetime] = Field(None,
                                                description="Filters for applications submitted on or after this date (greater than or equal to).")
    applied_at__lte: Optional[datetime] = Field(None,
                                                description="Filters for applications submitted on or before this date (less than or equal to).")

    created_at__gte: Optional[datetime] = Field(None,
                                                description="Filters for applications created in the system on or after this date (greater than or equal to).")
    created_at__lte: Optional[datetime] = Field(None,
                                                description="Filters for applications created in the system on or before this date (less than or equal to).")

    class Constants(Filter.Constants):
        model = ApplicationEntity