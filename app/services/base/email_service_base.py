from abc import ABC, abstractmethod

from app.configs.db.enums import ApplicationStatusEnum
from app.configs.kafka_configs.events.event_message_email import EventMessageEmail


class EmailServiceBase(ABC):

    @abstractmethod
    async def send_email_depend_application_status(self, user_email: str, status: ApplicationStatusEnum,
                                                   data: dict):
        pass

    @abstractmethod
    async def send_email_bye(self, user_email: str, subject: str, data: dict):
        pass

    @abstractmethod
    async def send_email_informing_application(self, user_email: str, subject: str, data: dict):
        pass

    @abstractmethod
    async def send_email_welcome_user(self, user_email: str, subject: str, data: dict):
        pass