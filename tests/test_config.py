"""Tests for configuration module."""

import os
import tempfile
from pathlib import Path

from src.config import Config


def test_config_default_logfile():
    """Test that config uses default logfile path when LOGFILE env var not set."""
    # Ensure LOGFILE env var is not set
    if "LOGFILE" in os.environ:
        del os.environ["LOGFILE"]

    config = Config()
    assert config.logfile == Path("data/govuk_stats_log.json")


def test_config_environment_logfile():
    """Test that config uses LOGFILE env var when set."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_logfile = Path(temp_dir) / "test.json"
        os.environ["LOGFILE"] = str(test_logfile)

        try:
            config = Config()
            assert config.logfile == test_logfile
        finally:
            del os.environ["LOGFILE"]


def test_config_creates_directories(tmp_path):
    """Test that config creates necessary directories."""
    test_logfile = tmp_path / "data" / "test.json"
    os.environ["LOGFILE"] = str(test_logfile)

    try:
        config = Config()

        # Check that directories were created
        assert config.logfile.parent.exists()
        assert config.plots_dir.exists()
    finally:
        del os.environ["LOGFILE"]


def test_config_plot_path():
    """Test that plot_path property returns correct path."""
    config = Config()
    expected = config.plots_dir / config.plot_filename
    assert config.plot_path == expected
    assert config.plot_path.name == "statistics.png"


def test_config_gov_url():
    """Test that gov_url is set correctly."""
    config = Config()
    assert config.gov_url == "https://www.gov.uk/search/research-and-statistics"


def test_config_datetime_format():
    """Test that datetime_format is set correctly."""
    config = Config()
    assert config.datetime_format == "%Y-%m-%d %H:%M:%S"


def test_config_datetime_format_environment():
    """Test that datetime_format can be overridden via environment."""
    custom_format = "%d/%m/%Y %H:%M"
    os.environ["DATETIME_FORMAT"] = custom_format

    try:
        config = Config()
        assert config.datetime_format == custom_format
    finally:
        del os.environ["DATETIME_FORMAT"]
