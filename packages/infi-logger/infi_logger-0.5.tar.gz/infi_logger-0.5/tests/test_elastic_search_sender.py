from unittest.mock import MagicMock, patch
from infi_logger.elastic_search_sender import ElasticSearchSender


def test_send_log(elastic_search_sender: ElasticSearchSender, log: dict[str, str]):
    with patch.object(
        elastic_search_sender, "_ElasticSearchSender__send_log"
    ) as mock_send_log:
        elastic_search_sender.send_log(log)

        mock_send_log.assert_called_once_with(log)


def test_send_log_to_elastic_success(
    elastic_search_sender: ElasticSearchSender, log: dict[str, str]
):
    mock_elasticsearch = MagicMock()
    elastic_search_sender.elasticsearch = mock_elasticsearch

    mock_local_logs_writer = MagicMock()
    elastic_search_sender.write_local_log = mock_local_logs_writer

    elastic_search_sender._ElasticSearchSender__send_log(log)

    mock_elasticsearch.send_log_to_elastic.assert_called_once_with(log)


def test_send_log_to_elastic_failure(
    elastic_search_sender: ElasticSearchSender, log: dict[str, str]
):
    mock_elasticsearch = MagicMock()
    mock_elasticsearch.send_log_to_elastic.side_effect = Exception("Connection error")
    elastic_search_sender.elasticsearch = mock_elasticsearch

    mock_local_logs_writer = MagicMock()
    elastic_search_sender.write_local_log = mock_local_logs_writer

    elastic_search_sender._ElasticSearchSender__send_log(log)

    mock_local_logs_writer.write_log.assert_called_once_with(log)
