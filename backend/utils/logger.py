import json
import logging
import sys
from datetime import datetime

def setup(level=logging.INFO) -> logging.Logger:
    """
    Set up and return a JSON-formatted logger.
    Safe to call multiple times — it won't duplicate handlers.
    """
    logger = logging.getLogger("pipeline")
    if logger.handlers:
        return logger
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            payload = {
                "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "level": record.levelname,
                "name": record.name,
                "msg": record.getMessage(),
            }
            if record.exc_info:
                payload["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(payload)

    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger
