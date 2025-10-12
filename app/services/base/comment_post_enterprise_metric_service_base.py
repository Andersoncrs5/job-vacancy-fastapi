from abc import ABC, abstractmethod

from app.configs.db.database import CommentPostEnterpriseMetricEntity
from app.utils.enums.sum_red import ColumnsCommentPostEnterpriseMetricEnum, SumRedEnum


class CommentPostEnterpriseMetricServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def delete(self, metric: CommentPostEnterpriseMetricEntity) -> None:
        pass

    @abstractmethod
    async def update_metric(self, comment_id: int, column: ColumnsCommentPostEnterpriseMetricEnum, action: SumRedEnum):
        pass

    @abstractmethod
    async def create(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        pass