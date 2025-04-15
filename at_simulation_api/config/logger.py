import json
import logging

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers.data import JsonLexer
from pythonjsonlogger import jsonlogger


def setup_logger(logger_name: str = "application_logger") -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()

    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def format(self, record):
            log_record = super().format(record)
            try:
                parsed = json.loads(log_record)
                formatted_json = json.dumps(parsed, indent=4)
                return highlight(formatted_json, JsonLexer(), TerminalFormatter())
            except Exception:
                return log_record

    formatter = CustomJsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s %(details)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)

application_logger = setup_logger()
