from aiokafka import AIOKafkaProducer

from app.configs.db.kafka import KAFKA_BROKER, KAFKA_TOPIC

producer: AIOKafkaProducer | None = None

async def get_producer() -> AIOKafkaProducer:
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
        await producer.start()
    return producer

async def send_message(value: str, topic: str = KAFKA_TOPIC):
    prod = await get_producer()
    await prod.send_and_wait(topic, value.encode("utf-8"))
