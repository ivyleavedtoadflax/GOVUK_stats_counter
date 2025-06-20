"""Tests for visualization module."""

import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from src.config import config
from src.create_visualization import format_thousands, load_data


def test_load_data_empty_file():
    """Test loading data from empty file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        temp_file = f.name

    try:
        timestamps, counts = load_data(temp_file)
        assert timestamps == []
        assert counts == []
    finally:
        Path(temp_file).unlink()


def test_load_data_valid_file():
    """Test loading data from valid JSON file."""
    test_data = [
        {"time": "2022-01-01 12:00:00", "count": 1000},
        {"time": "2022-02-01 12:00:00", "count": 1100},
        {"time": "2022-03-01 12:00:00", "count": 1200},
    ]

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        for entry in test_data:
            json.dump(entry, f)
            f.write("\n")
        temp_file = f.name

    try:
        timestamps, counts = load_data(temp_file)

        assert len(timestamps) == 3
        assert len(counts) == 3
        assert counts == [1000, 1100, 1200]

        # Check first timestamp
        expected_dt = datetime.strptime("2022-01-01 12:00:00", config.datetime_format)
        assert timestamps[0] == expected_dt
    finally:
        Path(temp_file).unlink()


def test_load_data_malformed_file():
    """Test loading data from file with malformed JSON."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write('{"time": "2022-01-01 12:00:00", "count": 1000}\n')
        f.write("invalid json line\n")
        f.write('{"time": "2022-03-01 12:00:00", "count": 1200}\n')
        temp_file = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_data(temp_file)
    finally:
        Path(temp_file).unlink()


def test_format_thousands():
    """Test thousands formatting function."""
    assert format_thousands(1000, None) == "1,000"
    assert format_thousands(1234567, None) == "1,234,567"
    assert format_thousands(500, None) == "500"
    assert format_thousands(0, None) == "0"


def test_format_thousands_float():
    """Test thousands formatting with float input."""
    assert format_thousands(1000.7, None) == "1,000"
    assert format_thousands(1234567.9, None) == "1,234,567"
