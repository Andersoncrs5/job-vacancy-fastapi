from app.configs.kafka_configs.events.base import EventBase


class EventMention(EventBase):
    names: list[str]
    entity_id: int