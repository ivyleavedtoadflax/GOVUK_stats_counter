# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a containerized Python application that automatically tracks the number of statistics published on GOV.UK over time. The project runs as a scheduled GitHub Actions job monthly on the 1st at 13:00 UTC to collect data points.

## Core Architecture

- **Main scraper**: `src/get_count.py` - Fetches statistics count from GOV.UK using dual-method extraction
- **Logging utility**: `src/write_json_log.py` - Appends timestamped data to JSON log file
- **Visualization**: `src/create_visualization.py` - Generates PNG plots of historical data
- **Configuration**: `src/config.py` - Pydantic-based configuration management
- **Data output**: `data/govuk_stats_log.json` - Time-series log of statistics counts
- **Plot output**: `plots/statistics.png` - Automated data visualization
- **Testing**: `tests/` - Comprehensive test suite (15 tests)
- **Automation**: `.github/workflows/cronjob.yml` - Monthly data collection via GitHub Actions
- **CI/CD**: `.github/workflows/test.yml` - Testing pipeline with ruff and pytest

## Data Extraction Strategy

The application scrapes `https://www.gov.uk/search/research-and-statistics` using robust dual-method extraction:

1. **Primary**: Meta tag `<meta name="govuk:search-result-count" content="96272">`
2. **Secondary**: Span element `<span class="js-result-count">96,272 results</span>`

This dual-method approach ensures reliability even when GOV.UK changes their page structure.

## Development Commands

### uv (Package Management)
```bash
# Install dependencies
uv sync

# Run the main scraper
uv run python src/get_count.py

# Add new dependencies
uv add <package-name>
```

### Docker Development
```bash
# Build the container
docker build -t govuk-stats-counter .

# Run with docker-compose (recommended)
docker-compose up

# Run standalone container
docker run -v $(pwd)/data:/app/data -v $(pwd)/plots:/app/plots govuk-stats-counter
```

## Environment Variables (Optional)

- `LOGFILE`: Path to the JSON log file (default: `data/govuk_stats_log.json`)
- `DATETIME_FORMAT`: Timestamp format string (default: `%Y-%m-%d %H:%M:%S`)
- `TZ`: Timezone setting (set to `Europe/London` in Docker)

## Key Dependencies

- `requests`: HTTP requests to GOV.UK
- `lxml`: HTML parsing and XPath extraction
- `matplotlib`: Data visualization and plot generation
- `pydantic-settings`: Configuration management with type validation
- `wasabi`: Logging utilities

## Data Format

The output JSON log contains one entry per line:
```json
{"time": "2025-06-20 08:54:53", "count": 96272}
```

## Current Status (June 2025)

- **System Status**: ✅ Fully operational
- **Latest Count**: 96,281+ statistics
- **Data Collection**: Automated monthly via GitHub Actions
- **Test Pipeline**: ✅ All tests passing
- **Recent Fixes**: Updated scraping logic, migrated to uv, fixed Docker issues

## Workflows

### CronJob Workflow (.github/workflows/cronjob.yml)
- **Trigger**: Monthly on the 1st at 13:00 UTC
- **Purpose**: Automated data collection
- **Process**: Builds Docker container, runs scraper, commits new data and plots
- **Status**: ✅ Working (resumed June 2025 after fixes)

### Test Workflow (.github/workflows/test.yml)
- **Trigger**: Every push and pull request
- **Purpose**: CI/CD testing pipeline
- **Tests**: Ruff linting/formatting, pytest (15 tests), Docker build/run verification
- **Status**: ✅ All tests passing