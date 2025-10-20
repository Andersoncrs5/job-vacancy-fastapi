from datetime import datetime

from app.configs.db.enums import NotificationTypeEnum
from app.configs.orjson.orjson_config import ORJSONModel
from app.schemas.base import NotificationBaseOUT

class NotificationEnterpriseOUT(NotificationBaseOUT):
    enterprise_id: int
