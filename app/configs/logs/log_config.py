import structlog
import logging
from structlog.processors import TimeStamper, KeyValueRenderer
from structlog.stdlib import LoggerFactory, add_log_level
from structlog.contextvars import merge_contextvars
from structlog.typing import BindableLogger


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO
    )

    structlog.configure(
        processors=[
            merge_contextvars,
            add_log_level,
            TimeStamper(fmt="iso", utc=True),
            KeyValueRenderer(
                key_order=['timestamp', 'level', 'event'],
                sort_keys=False
            ),
        ],
        logger_factory=LoggerFactory(),
        #wrapper_class=BindableLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()