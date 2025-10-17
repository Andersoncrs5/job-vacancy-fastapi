import json
from pathlib import Path
import time
from typing import Final, List

import structlog
from aiokafka import AIOKafkaProducer
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError, NoBrokersAvailable

KAFKA_BROKER: Final[str] = "localhost:29092"

SUM_RED_METRIC_TOPIC: Final[str] = "sum_red_metric_topic"
SEND_EMAIL_TOPIC: Final[str] = "send_email_topic"
NOTIFICATION_TOPIC: Final[str] = "notification_topic"

producer: AIOKafkaProducer | None = None

CURRENT_DIR = Path(__file__).parent
TOPICS_CONFIG_FILE = CURRENT_DIR / "topics.json"

logger = structlog.get_logger()

class KafkaAdmin:

    MAX_RETRIES = 5
    RETRY_DELAY_SEC = 2

    CREATE_TOPIC_TIMEOUT_MS = 10000

    def __init__(self, bootstrap_servers: list[str]):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = self._initialize_admin_client(bootstrap_servers)

    def _initialize_admin_client(self, bootstrap_servers: List[str]) -> KafkaAdminClient:
        """Inicializa o AdminClient com retentativas para lidar com problemas de conexão."""
        logger.info("Attempting to initialize Kafka AdminClient with retries...")

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:

                admin_client = KafkaAdminClient(
                    bootstrap_servers=bootstrap_servers,
                    client_id='vacancy-job-fastapi-admin-client',


                    request_timeout_ms=5000,
                )
                logger.info("Kafka AdminClient initialized successfully.", attempt=attempt)
                return admin_client

            except (NoBrokersAvailable, KafkaError) as e:
                logger.warning(
                    "Kafka broker connection failed.",
                    attempt=attempt,
                    max_attempts=self.MAX_RETRIES,
                    error=str(e)
                )
                if attempt == self.MAX_RETRIES:
                    logger.critical("Failed to connect to Kafka after multiple retries. Aborting application startup.",
                                    exc_info=True)

                    raise RuntimeError(f"Cannot connect to Kafka broker at {bootstrap_servers}") from e


                time.sleep(self.RETRY_DELAY_SEC)
            except Exception as e:

                logger.error("Unexpected error during Kafka AdminClient initialization.", error=str(e), exc_info=True)

                raise RuntimeError(f"Unexpected Kafka initialization error: {e}") from e


        raise RuntimeError("Failed to initialize Kafka AdminClient.")

    def _read_topics_config(self) -> list[dict]:
        """Lê o arquivo de configuração de tópicos de forma robusta."""

        if not TOPICS_CONFIG_FILE.exists():

            logger.error(
                "topics.json not found",
                file_path=str(TOPICS_CONFIG_FILE.resolve())
            )
            return []

        try:
            with open(TOPICS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("topics", [])
        except json.JSONDecodeError as e:

            logger.error(
                "Error decoding topics.json file.",
                error=str(e),
                file_path=str(TOPICS_CONFIG_FILE)
            )
            return []

    def create_topics_from_file(self):
        """Executa a lógica de criação de tópicos (síncrona)."""
        topic_configs = self._read_topics_config()
        if not topic_configs:
            logger.warning("No topic configurations found, skipping initialization.")
            return

        logger.info("Starting Kafka Admin initialization.", bootstrap_servers=self.bootstrap_servers)

        new_topics = []
        for config in topic_configs:


            replication_factor = config.get('replication_factor', 1)

            if replication_factor > 1:
                logger.warning(
                    "Replication factor capped at 1.",
                    reason="Single broker assumed for local development.",
                    original_factor=replication_factor,
                    topic_name=config['name']
                )
                replication_factor = 1


            logger.info("Preparing topic configuration.", topic_name=config['name'])

            new_topics.append(NewTopic(
                name=config['name'],
                num_partitions=config.get('partitions', 1),
                replication_factor=replication_factor
            ))

        try:

            futures = self.admin_client.create_topics(
                new_topics=new_topics,
                validate_only=False,
                timeout_ms=self.CREATE_TOPIC_TIMEOUT_MS
            )


            for topic_name, future in futures.items():
                try:

                    future.get(timeout=(self.CREATE_TOPIC_TIMEOUT_MS / 1000))

                    logger.info("Topic created successfully.", topic_name=topic_name)
                except TopicAlreadyExistsError:
                    logger.info("Topic already exists. Proceeding.", topic_name=topic_name, action="skip")
                except KafkaError as e:

                    logger.error("Failed to process topic.", topic_name=topic_name, error=str(e))
                except Exception as e:

                    logger.error("Unexpected error during topic creation.", topic_name=topic_name, error=str(e),
                                 exc_info=e)

        except TopicAlreadyExistsError as e:


            logger.warning(
                "AdminClient raised TopicAlreadyExistsError.",
                reason="One or more topics already existed on the broker. This is expected in repeated runs.",
                error=str(e)
            )

        except Exception as e:

            logger.critical(
                "Fatal error communicating with Kafka AdminClient during topic creation.",
                error=str(e),
                servers=self.bootstrap_servers,
                exc_info=e
            )

        finally:
            pass