"""Utility function to write logs to json."""

import json
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def write_json_log(data, log_file):
    """
    Write log data to json file.

    Args:
        data (dict): Dict to append to json file.
        log_file (str): Path to data file.

    Returns:
        None
    """

    try:
        # Ensure parent directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, "a") as lf:
            json.dump(data, lf)
            lf.write("\n")
        logger.info(f"Wrote log file to {log_file}")
    except Exception:
        logger.exception("write_json_log: Failed to log data to log")
