# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a containerized Python application that scrapes the number of statistics published on GOV.UK and logs the data to a JSON file. The project is designed to run as a scheduled job or cron task to track statistics counts over time.

## Core Architecture

- **Main scraper**: `src/get_count.py` - Fetches statistics count from GOV.UK search page using XPath
- **Logging utility**: `src/write_json_log.py` - Appends timestamped data to JSON log file
- **Data output**: `data/govuk_stats_log.json` - Time-series log of statistics counts

The application scrapes `https://www.gov.uk/search/research-and-statistics`, extracts the result count using XPath `//*[(@id = "js-result-count")]/text()`, and logs it with a timestamp.

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
docker run -v $(pwd)/data:/data -e LOGFILE=/data/govuk_stats_log.json govuk-stats-counter
```

## Environment Variables

- `LOGFILE`: Path to the JSON log file (default: `/data/govuk_stats_log.json`)
- `TZ`: Timezone setting (set to `Europe/London` in Docker)

## Key Dependencies

- `requests`: HTTP requests to GOV.UK
- `lxml`: HTML parsing and XPath extraction
- `wasabi`: Logging utilities

## Data Format

The output JSON log contains one entry per line:
```json
{"time": "2024-01-01 12:00:00", "count": 12345}
```