import json
import os
import logging

from infi_logger.consts import LogConsts

# Define a constant for the default path where failed logs will be stored
DEFAULT_PATH = LogConsts.DEFAULT_PATH


# LocalLogsWriter class responsible for writing logs locally
class LocalLogsWriter:
    def __init__(self) -> None:
        # Initialize an instance of the LocalLogsWriter class
        self.path = DEFAULT_PATH

    def set_log_directory(self, new_directory):
        """
        Set a new directory for storing failed logs.

        Parameters:
        - new_directory (str): The new directory path.
        """
        # Update the log file path with the new directory
        if new_directory:
            self.path = os.path.join(new_directory, os.path.basename(self.path))
            # Create the new directory if it doesn't exist
            self.__create_failed_log_dir(new_directory)

    def write_log(self, log: dict):
        # Convert the log dictionary to a JSON string
        log_string = json.dumps(log)

        # Ensure the directory exists before attempting to write the log file
        self.__create_failed_log_dir(os.path.dirname(self.path))

        # Append the JSON string to the log file
        with open(self.path, mode="a", encoding="utf-8") as file:
            file.write(f"{log_string}\n")
            logging.info(f"Log written to {self.path}")

    @staticmethod
    def __create_failed_log_dir(directory_path):
        # Create the specified directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)
