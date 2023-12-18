from infi_logger.elastic_logger import ElasticLogger
from unittest.mock import MagicMock, ANY


def test_elastic_logger():
    elastic_logger = ElasticLogger("my_service")
    assert elastic_logger.service_name == "my_service"


def test_create_log(elastic_logger: ElasticLogger):
    new_log = elastic_logger._ElasticLogger__create_log("my-log", "INFO")
    assert new_log["message"] == "my-log"
    assert new_log["level"] == "INFO"
    assert new_log["service"] == "test-service"


def test_send_log(elastic_logger: ElasticLogger):
    elastic_logger.sender = MagicMock()
    elastic_logger._ElasticLogger__send_log("Test message", "DEBUG")
    elastic_logger.sender.send_log.assert_called_once_with(
        {
            "timestamp": ANY,
            "message": "Test message",
            "level": "DEBUG",
            "service": "test-service",
        }
    )


def test_debug(elastic_logger: ElasticLogger):
    send_log_mock = MagicMock()
    elastic_logger._ElasticLogger__send_log = send_log_mock
    elastic_logger.debug("Test message")
    send_log_mock.assert_called_once_with("Test message", "DEBUG")


def test_info(elastic_logger: ElasticLogger):
    send_log_mock = MagicMock()
    elastic_logger._ElasticLogger__send_log = send_log_mock
    elastic_logger.info("Test message")
    send_log_mock.assert_called_once_with("Test message", "INFO")


def test_warning(elastic_logger: ElasticLogger):
    send_log_mock = MagicMock()
    elastic_logger._ElasticLogger__send_log = send_log_mock
    elastic_logger.warning("Test message")
    send_log_mock.assert_called_once_with("Test message", "WARNING")


def test_error(elastic_logger: ElasticLogger):
    send_log_mock = MagicMock()
    elastic_logger._ElasticLogger__send_log = send_log_mock
    elastic_logger.error("Test message")
    send_log_mock.assert_called_once_with("Test message", "ERROR")


def test_critical(elastic_logger: ElasticLogger):
    send_log_mock = MagicMock()
    elastic_logger._ElasticLogger__send_log = send_log_mock
    elastic_logger.critical("Test message")
    send_log_mock.assert_called_once_with("Test message", "CRITICAL")
