import logging
from elasticsearch import Elasticsearch


class ElasticsearchConnection:
    def __init__(
        self, host=None, cert_fingerprint=None, name=None, password=None, index=None
    ) -> None:
        self.host = host
        self.cert_fingerprint = cert_fingerprint
        self.name = name
        self.password = password
        self.index = index
        self.is_connected = False
        self.elasticsearch = None

        if all([host, name, password, index]):
            self.connect_elasticsearch()

    def connect_elasticsearch(self) -> None:
        if not all([self.host, self.name, self.password, self.index]):
            self.is_connected = False
            raise ValueError("Missing required parameters for Elasticsearch connection")

        try:
            self.elasticsearch = self.init_elasticsearch()
            self.is_connected = self.__check_connection()
        except Exception as e:
            logging.error(f"Error connecting to Elasticsearch: {e}")
            self.elasticsearch = None
            self.is_connected = False

    def init_elasticsearch(self) -> Elasticsearch:
        try:
            return Elasticsearch(
                [self.host],
                ssl_assert_fingerprint=self.cert_fingerprint,
                basic_auth=(self.name, self.password),
            )
        except Exception as e:
            logging.error(f"Error initializing Elasticsearch client: {e}")
            raise

    def __check_connection(self) -> bool:
        res = self.elasticsearch.ping()
        if res is False:
            logging.error(self.elasticsearch.info())
        return res

    def send_log_to_elastic(self, log) -> None:
        if not self.is_active_connection():
            raise Exception("Elasticsearch is not connected")
        try:
            res = self.elasticsearch.index(index=self.index, body=log)
            if res["result"] != "created":
                raise Exception(f'Log was not sent. res = {res["result"]}')
        except Exception as e:
            logging.error(f"Error sending log to Elasticsearch: {e}")
            raise e

    def is_active_connection(self) -> bool:
        if not self.is_connected:
            self.connect_elasticsearch()
        return self.is_connected
