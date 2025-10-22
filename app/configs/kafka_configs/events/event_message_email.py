from datetime import datetime
from enum import Enum
from uuid import UUID

from app.configs.kafka_configs.events.base import EventBase
from app.configs.orjson.orjson_config import ORJSONModel

class TemplateEnum(str, Enum):
    welcome_email = 'welcome_email'
    order_confirmation = 'order_confirmation'
    email_bye = 'email_bye'
    informing_application = 'informing_application'
    interview_scheduled = 'interview_scheduled'
    offer_extended = 'offer_extended'
    hired_confirmation = 'hired_confirmation'
    rejected_application = 'rejected_application'

class EventMessageEmail(EventBase):
    email: str
    template_name: TemplateEnum
    subject: str
    cc: list[str] | None = None,
    bcc: list[str] | None = None