import os


class LogConsts:
    DEFAULT_PATH = os.environ.get("LOG_FILE", "logs/log.log")
