import logging
from logging import Logger


class PyLoxLogger:
    def __init__(self) -> None:
        self._log: Logger = _instanciate_log("PyLox")

    def lineError(self, line: int, message: str) -> None:
        self._log.error("{ Line %s } Error: %s" % str(line), message)

    def info(self, message: str) -> None:
        self._log.info(message)

    def error(self, message: str) -> None:
        self._log.error(message)


def _instanciate_log(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f"[{name}] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
