"""Configuration management for GOV.UK statistics counter."""

from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration with sensible defaults."""

    # Scraping configuration
    gov_url: str = "https://www.gov.uk/search/research-and-statistics"

    # Data file configuration
    logfile: Path = Field(default=Path("data/govuk_stats_log.json"))
    datetime_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Format string for timestamps in log files",
    )

    # Output configuration
    plots_dir: Path = Field(default=Path("plots"))
    plot_filename: str = "statistics.png"

    def model_post_init(self, __context) -> None:
        """Ensure required directories exist after initialization."""
        # Ensure data directory exists
        self.logfile.parent.mkdir(parents=True, exist_ok=True)

        # Ensure plots directory exists
        self.plots_dir.mkdir(parents=True, exist_ok=True)

    @computed_field
    @property
    def plot_path(self) -> Path:
        """Get the full path to the plot file."""
        return self.plots_dir / self.plot_filename


# Global configuration instance
config = Config()
