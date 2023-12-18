from datetime import datetime

from infi_logger.elastic_search_sender import ElasticSearchSender


class ElasticLogger:
    def __init__(
        self,
        service_name,
        host="http://localhost:9200",
        cert_fingerprint=None,
        username=None,
        password=None,
        index=None,
    ) -> None:
        self.service_name = service_name
        self.sender = ElasticSearchSender(
            host=host,
            cert_fingerprint=cert_fingerprint,
            username=username,
            password=password,
            index=index,
        )

    def debug(self, message):
        self.__send_log(message, "DEBUG")

    def info(self, message):
        self.__send_log(message, "INFO")

    def warning(self, message):
        self.__send_log(message, "WARNING")

    def error(self, message):
        self.__send_log(message, "ERROR")

    def critical(self, message):
        self.__send_log(message, "CRITICAL")

    def set_log_path(self, path):
        self.sender.write_local_log.path = path

    def __send_log(self, message, level):
        message = str(message)
        log = self.__create_log(message, level)
        print(message)
        self.sender.send_log(log)

    def __create_log(self, message, level):
        return {
            "timestamp": f"{datetime.now().isoformat()}",
            "message": message,
            "level": level,
            "service": self.service_name,
        }
