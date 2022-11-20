"""
Utility function to write logs to json for reading by telegraf
"""

import json
from logging import getLogger

logger = getLogger(__name__)


def write_json_log(data, log_file):
    """
    Write log data to csv
    
    Args:
        data (dict): Dict to append to json file.
        log_file (str): Path to data file.

    Returns:
        None
    """

    try:
        with open(log_file, "a") as lf:
            json.dump(data, lf)
            lf.write("\n")
        logger.info(f"Wrote log file to {log_file}")
    except Exception:
        logger.exception("write_json_log: Failed to log data to log")
