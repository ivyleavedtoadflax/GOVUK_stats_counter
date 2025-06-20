"""Configuration management for GOV.UK statistics counter."""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Application configuration with sensible defaults."""

    # Scraping configuration
    gov_url: str = "https://www.gov.uk/search/research-and-statistics"

    # Output configuration
    plots_dir: Path = field(default_factory=lambda: Path("plots"))
    plot_filename: str = "statistics.png"

    # Data file configuration (computed from environment)
    logfile: Path = field(init=False)

    def __post_init__(self):
        """Initialize computed fields and ensure directories exist."""
        self.logfile = self._get_logfile_path()
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
