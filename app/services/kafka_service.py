from aiokafka import AIOKafkaProducer
from app.configs.kafka.kafka import KAFKA_BROKER

async def get_producer_dependency():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)

    await producer.start()

    try:
        yield producer
    finally:
        await producer.stop()

async def send_message_to_kafka(prod: AIOKafkaProducer, value: str, topic: str):
    await prod.send_and_wait(topic, value.encode("utf-8"))