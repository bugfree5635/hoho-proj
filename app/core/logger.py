import json
import logging

from app.core.request_context import request_id_context


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": request_id_context.get(),
        }

        return json.dumps(log_data)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.handlers.clear()
    logger.addHandler(handler)
