"""Tests for JSON logging functionality."""

import json
import tempfile
from pathlib import Path

from src.write_json_log import write_json_log


def test_write_json_log_new_file():
    """Test writing to a new log file."""
    test_data = {"time": "2022-01-01 12:00:00", "count": 1000}

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        temp_file = f.name

    # Remove the file so we can test creating a new one
    Path(temp_file).unlink()

    try:
        write_json_log(test_data, log_file=temp_file)

        # Verify the file was created and contains correct data
        assert Path(temp_file).exists()

        with open(temp_file) as f:
            content = f.read().strip()
            loaded_data = json.loads(content)
            assert loaded_data == test_data
    finally:
        if Path(temp_file).exists():
            Path(temp_file).unlink()


def test_write_json_log_append_to_existing():
    """Test appending to an existing log file."""
    initial_data = {"time": "2022-01-01 12:00:00", "count": 1000}
    new_data = {"time": "2022-02-01 12:00:00", "count": 1100}

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        json.dump(initial_data, f)
        f.write("\n")
        temp_file = f.name

    try:
        write_json_log(new_data, log_file=temp_file)

        # Verify both entries are in the file
        with open(temp_file) as f:
            lines = f.read().strip().split("\n")
            assert len(lines) == 2

            assert json.loads(lines[0]) == initial_data
            assert json.loads(lines[1]) == new_data
    finally:
        if Path(temp_file).exists():
            Path(temp_file).unlink()


def test_write_json_log_creates_parent_directories():
    """Test that write_json_log creates parent directories if they don't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = Path(temp_dir) / "subdir" / "test.json"
        test_data = {"time": "2022-01-01 12:00:00", "count": 1000}

        # Ensure the subdirectory doesn't exist
        assert not log_file.parent.exists()

        write_json_log(test_data, log_file=str(log_file))

        # Verify the file and directory were created
        assert log_file.exists()
        assert log_file.parent.exists()

        with open(log_file) as f:
            content = f.read().strip()
            loaded_data = json.loads(content)
            assert loaded_data == test_data
