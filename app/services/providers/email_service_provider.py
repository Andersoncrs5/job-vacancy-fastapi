import datetime
import uuid

from aiokafka import AIOKafkaProducer

from app.configs.db.enums import ApplicationStatusEnum
from app.configs.kafka_configs.events.event_message_email import EventMessageEmail, TemplateEnum
from app.configs.kafka_configs.kafka_admin import SEND_EMAIL_TOPIC
from app.services.base.email_service_base import EmailServiceBase
from app.services.kafka_service import send_message_to_kafka


class EmailServiceProvider(EmailServiceBase):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send_email_depend_application_status(
        self,
        user_email: str,
        status: ApplicationStatusEnum,
        data: dict
    ):
        subject_map = {
            ApplicationStatusEnum.INTERVIEWING: f"Interview Request for {data['vacancy']['title']}!",
            ApplicationStatusEnum.OFFER_EXTENDED: f"Job Offer for the {data['vacancy']['title']} Position!",
            ApplicationStatusEnum.HIRED: f"Congratulations! Welcome to the Team!",
            ApplicationStatusEnum.REJECTED: f"Update on your Application for {data['vacancy']['title']}",
        }

        template_map = {
            ApplicationStatusEnum.INTERVIEWING: TemplateEnum.interview_scheduled,
            ApplicationStatusEnum.OFFER_EXTENDED: TemplateEnum.offer_extended,
            ApplicationStatusEnum.HIRED: TemplateEnum.hired_confirmation,
            ApplicationStatusEnum.REJECTED: TemplateEnum.rejected_application,
        }

        if status not in template_map:
            return

        event = EventMessageEmail(
            event_id=uuid.uuid4(),
            email=user_email,
            template_name=template_map[status],
            subject=subject_map[status],
            created_at=datetime.datetime.now(),
            source_service='email-service-provider|send_email_depend_application_status',
            data=data,
            cc=None,
            bcc=None,
            metadata={},
        )

        # await send_message_to_kafka(self.producer, event.model_dump_json(), SEND_EMAIL_TOPIC)

    async def send_email_informing_application(self, user_email: str, subject: str, data: dict):
        event = EventMessageEmail(
            event_id=uuid.uuid4(),
            email=user_email,
            template_name=TemplateEnum.informing_application,
            created_at=datetime.datetime.now(),
            source_service='email-service-provider|send_email_informing_application',
            subject=subject,
            cc=None,
            bcc=None,
            data=data,
            metadata={},
        )

        # await send_message_to_kafka(self.producer, event.model_dump_json(), SEND_EMAIL_TOPIC)

    async def send_email_bye(self, user_email: str, subject: str, data: dict):
        event = EventMessageEmail(
            event_id=uuid.uuid4(),
            email=user_email,
            template_name=TemplateEnum.email_bye,
            created_at=datetime.datetime.now(),
            source_service='email-service-provider|send_email_bye',
            subject=subject,
            cc=None,
            bcc=None,
            data=data,
            metadata={},
        )

        # await send_message_to_kafka(self.producer, event.model_dump_json(), SEND_EMAIL_TOPIC)

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

        # await send_message_to_kafka(self.producer, event.model_dump_json(), SEND_EMAIL_TOPIC)