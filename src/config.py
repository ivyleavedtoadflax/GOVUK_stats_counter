"""Configuration management for GOV.UK statistics counter."""

import os
from pathlib import Path


class Config:
    """Application configuration with sensible defaults."""

    def __init__(self):
        # Data file configuration
        self.logfile = self._get_logfile_path()

        # Scraping configuration
        self.gov_url = "https://www.gov.uk/search/research-and-statistics"

        # Output configuration
        self.plots_dir = Path("plots")
        self.plot_filename = "statistics.png"

        # Ensure output directories exist
        self._ensure_directories()

    def _get_logfile_path(self) -> Path:
        """Get the log file path from environment or use default."""
        env_logfile = os.environ.get("LOGFILE")
        if env_logfile:
            return Path(env_logfile)

        # Default to data directory for local development
        return Path("data/govuk_stats_log.json")

    def _ensure_directories(self):
        """Ensure required directories exist."""
        # Ensure data directory exists
        self.logfile.parent.mkdir(exist_ok=True)

        # Ensure plots directory exists
        self.plots_dir.mkdir(exist_ok=True)

    @property
    def plot_path(self) -> Path:
        """Get the full path to the plot file."""
        return self.plots_dir / self.plot_filename


# Global configuration instance
config = Config()
