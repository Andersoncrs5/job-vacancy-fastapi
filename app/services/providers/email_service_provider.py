import datetime
import uuid

from aiokafka import AIOKafkaProducer

from app.configs.kafka_configs.events.event_message_email import EventMessageEmail, TemplateEnum
from app.configs.kafka_configs.kafka_admin import SEND_EMAIL_TOPIC
from app.services.base.email_service_base import EmailServiceBase
from app.services.kafka_service import send_message_to_kafka


class EmailServiceProvider(EmailServiceBase):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send_email_welcome_user(self, user_email: str, subject: str, data: dict):
        event = EventMessageEmail(
            event_id = uuid.uuid4(),
            email = user_email,
            template_name = TemplateEnum.welcome_email,
            created_at = datetime.datetime.now(),
            source_service = 'email-service-provider|send-email-welcome-user',
            subject = subject,
            cc = None,
            bcc = None,
            data = data,
            metadata = {},
        )

        await send_message_to_kafka(self.producer, event.model_dump_json(), SEND_EMAIL_TOPIC)