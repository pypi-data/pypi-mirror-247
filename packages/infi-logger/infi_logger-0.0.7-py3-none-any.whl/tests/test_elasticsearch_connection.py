from unittest.mock import MagicMock, Mock
from infi_logger.elasticsearch_connection import ElasticsearchConnection
import pytest


def test_connect_elasticsearch(
    elasticsearch_connection: ElasticsearchConnection, mock_es_instance
):
    mock_es_instance.ping.return_value = True

    # Call connect_elasticsearch, which returns None
    elasticsearch_connection.connect_elasticsearch()

    # Assert that is_connected is True after a successful connection
    assert elasticsearch_connection.is_connected is True

    # Now, let's test the case where required parameters are missing
    # In this case, connect_elasticsearch should raise a ValueError
    elasticsearch_connection.name = None
    with pytest.raises(ValueError):
        elasticsearch_connection.connect_elasticsearch()

    # After the ValueError, is_connected should be False
    assert elasticsearch_connection.is_connected is False


def test__check_connection_success(sender: ElasticsearchConnection, mock_es_instance):
    mock_es_instance.ping.return_value = True

    assert sender._ElasticsearchConnection__check_connection() == True


def test__check_connection_not_success(
    sender: ElasticsearchConnection, mock_es_instance
):
    mock_es_instance.ping.return_value = False
    assert sender._ElasticsearchConnection__check_connection() == False


def test_send_log_to_elastic_not_success(
    sender: ElasticsearchConnection, mock_es_instance
):
    mock_es_instance.ping.return_value = True
    with pytest.raises(Exception) as excexption:
        sender.send_log_to_elastic("not send")
        assert str(excexption.value) == "Exception: The log was not sent"


def test_connect_elasticsearch_false(sender: ElasticsearchConnection):
    sender._ElasticsearchConnection__check_connection = MagicMock(return_value=False)
