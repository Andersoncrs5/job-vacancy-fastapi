from abc import ABC, abstractmethod

from app.configs.kafka_configs.events.event_message_email import EventMessageEmail


class EmailServiceBase(ABC):

    @abstractmethod
    async def send_email_welcome_user(self, user_email: str, subject: str, data: dict):
        pass