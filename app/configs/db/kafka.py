from typing import Final
from aiokafka import AIOKafkaProducer

KAFKA_BROKER: Final[str] = "localhost:29092"
KAFKA_TOPIC: Final[str] = "job_vacancy_topic"

# NÃO inicialize aqui. Apenas declare o tipo
producer: AIOKafkaProducer | None = None
