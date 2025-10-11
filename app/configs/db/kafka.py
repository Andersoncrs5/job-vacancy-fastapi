from typing import Final
from aiokafka import AIOKafkaProducer

KAFKA_BROKER: Final[str] = "localhost:29092"
SUM_RED_METRIC_TOPIC: Final[str] = "sum_red_metric_topic"

producer: AIOKafkaProducer | None = None
