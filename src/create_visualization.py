#!/usr/bin/env python3
"""
Create visualization of GOV.UK statistics count over time.

Reads the JSON log file and creates a line plot showing the growth
of statistics published on GOV.UK.
"""

import json
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from src.config import config


def load_data(log_file_path: str) -> tuple[list, list]:
    """Load timestamps and counts from JSON log file."""
    timestamps = []
    counts = []

    with open(log_file_path) as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                timestamp = datetime.strptime(data["time"], config.datetime_format)
                timestamps.append(timestamp)
                counts.append(data["count"])

    return timestamps, counts


def format_thousands(x, pos):
    """Format y-axis labels with thousands separator."""
    return f"{int(x):,}"


def create_plot(timestamps: list, counts: list, output_path: str) -> None:
    """Create and save the statistics visualization."""
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the data
    ax.plot(timestamps, counts, linewidth=2, color="#1f77b4", marker="o", markersize=3)

    # Customize the plot
    ax.set_title(
        "GOV.UK Statistics Count Over Time", fontsize=16, fontweight="bold", pad=20
    )
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Number of Statistics", fontsize=12)

    # Format y-axis with thousands separator
    ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator([1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Add grid
    ax.grid(True, alpha=0.3)

    # Improve layout
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Add latest count as annotation
    if timestamps and counts:
        latest_timestamp = timestamps[-1]
        latest_count = counts[-1]
        ax.annotate(
            f"Latest: {latest_count:,}\n{latest_timestamp.strftime('%Y-%m-%d')}",
            xy=(latest_timestamp, latest_count),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.7),
            fontsize=10,
        )

    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Visualization saved to: {output_path}")


def main():
    """Main function to create the visualization."""
    log_file = config.logfile
    output_path = config.plot_path

    if not log_file.exists():
        print(f"Error: Log file not found at {log_file}")
        return

    try:
        timestamps, counts = load_data(str(log_file))

        if not timestamps:
            print("No data found in log file")
            return

        create_plot(timestamps, counts, str(output_path))
        print(f"Successfully created visualization with {len(timestamps)} data points")

    except Exception as e:
        print(f"Error creating visualization: {e}")
        raise


if __name__ == "__main__":
    main()
