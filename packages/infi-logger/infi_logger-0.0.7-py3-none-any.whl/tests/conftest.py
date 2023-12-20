import pytest
from datetime import datetime
from unittest.mock import MagicMock
from infi_logger.elastic_logger import ElasticLogger
from infi_logger.local_logs_writer import LocalLogsWriter
from infi_logger.elastic_search_sender import ElasticSearchSender
from infi_logger.elasticsearch_connection import ElasticsearchConnection


@pytest.fixture(scope="session")
def elastic_logger():
    logger = ElasticLogger("test-service")
    yield logger


@pytest.fixture
def local_logs_writer():
    writer = LocalLogsWriter()
    yield writer


@pytest.fixture
def elastic_search_sender():
    sender = ElasticSearchSender()
    yield sender


@pytest.fixture
def log():
    log_json = {
        "timestamp": f"{datetime.now().isoformat()}",
        "message": "Test message",
        "level": "DEBUG",
        "service": "test-service",
    }
    return log_json


@pytest.fixture
def mock_es_instance():
    return MagicMock()


@pytest.fixture
def sender(mock_es_instance):
    sender_instance = ElasticsearchConnection()
    sender_instance.elasticsearch = mock_es_instance
    yield sender_instance


HOST = "https://localhost:9200"
CERT_FINGERPRINT = "275494d2581da06cc789a065c3d4be6475da532ee9d9484a4577a85ded291d7a"
NAME = "elastic"  # Elasticsearch username
PASSWORD = "Ofog_+xZV+9_ONrCWnh_"
INDEX = "test"  # Replace with the index you want to work with


# Update the elasticsearch_connection fixture to provide an ElasticsearchConnection instance
@pytest.fixture
def elasticsearch_connection():
    yield ElasticsearchConnection(
        host=HOST,
        cert_fingerprint=CERT_FINGERPRINT,
        name=NAME,
        password=PASSWORD,
        index=INDEX,
    )
