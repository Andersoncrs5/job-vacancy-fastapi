from abc import ABC, abstractmethod
from typing import List
from app.configs.db.database import ReviewEnterprise
from app.utils.filter.review_enterprise_filter import ReviewEnterpriseFilter

class ReviewEnterpriseRepositoryBase(ABC):

    @abstractmethod
    async def exists_by_user_id(self, user_id: int) -> bool:
        pass
