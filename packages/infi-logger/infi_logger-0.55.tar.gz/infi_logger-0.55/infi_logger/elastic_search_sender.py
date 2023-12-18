import threading
import logging

from infi_logger.elasticsearch_connection import ElasticsearchConnection
from infi_logger.local_logs_writer import LocalLogsWriter

lock = threading.Lock()


class ElasticSearchSender:
    def __init__(
        self, host=None, cert_fingerprint=None, username=None, password=None, index=None
    ) -> None:
        self.elasticsearch = ElasticsearchConnection(
            host=host,
            cert_fingerprint=cert_fingerprint,
            name=username,
            password=password,
            index=index,
        )
        self.write_local_log = LocalLogsWriter()

    def send_log(self, log):
        thread = threading.Thread(target=self.__send_log, args=(log,))
        thread.start()

    def __send_log(self, log):
        with lock:
            if self.elasticsearch.elasticsearch is None:  # Never initialized
                logging.info("ElasticSearch is not connected. Sending log")
                self.write_local_log.write_log(log)
            else:
                try:
                    self.elasticsearch.send_log_to_elastic(log)
                    logging.info("Log sent successfully to Elasticsearch.")
                except Exception as e:
                    logging.error(f"Error sending log to Elasticsearch: {e}")
                    self.write_local_log.write_log(log)
