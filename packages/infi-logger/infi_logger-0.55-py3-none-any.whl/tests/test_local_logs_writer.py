import os
import json
import pytest
from unittest.mock import patch

from infi_logger.local_logs_writer import LocalLogsWriter


@pytest.fixture
def logs_writer():
    return LocalLogsWriter()


def test_default_log_path(logs_writer):
    assert logs_writer.path == "failed_logs/failed_logs.log"


def test_set_log_directory(logs_writer, tmpdir):
    new_directory = str(tmpdir.mkdir("new_logs"))
    logs_writer.set_log_directory(new_directory)
    assert logs_writer.path == os.path.join(new_directory, "failed_logs.log")
    assert os.path.exists(new_directory)


def test_write_log(logs_writer, tmpdir):
    log_data = {"message": "Test log message", "level": "info"}
    expected_log_string = json.dumps(log_data) + "\n"

    new_directory = str(tmpdir.mkdir("logs"))
    logs_writer.set_log_directory(new_directory)

    with patch("builtins.open", create=True) as mock_open:
        logs_writer.write_log(log_data)

    mock_open.assert_called_once_with(
        os.path.join(new_directory, "failed_logs.log"), mode="a", encoding="utf-8"
    )
    handle = mock_open.return_value.__enter__.return_value
    handle.write.assert_called_once_with(expected_log_string)


@patch("os.makedirs")
def test_create_failed_log_dir(mock_makedirs, logs_writer, tmpdir):
    new_directory = str(tmpdir.mkdir("logs"))
    logs_writer._LocalLogsWriter__create_failed_log_dir(new_directory)
    mock_makedirs.assert_called_once_with(new_directory, exist_ok=True)
