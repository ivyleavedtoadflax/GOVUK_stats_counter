"""
GOV.UK statistics count go getter

Scrape the statistics count from the GOV.UK statistics homepage and
log it to json.
"""

import re
from logging import getLogger
from time import strftime

import requests
from lxml import html

from src.config import config
from src.create_visualization import main as create_visualization
from src.write_json_log import write_json_log

logger = getLogger(__name__)

try:
    page = requests.get(config.gov_url)
    tree = html.fromstring(page.content)

    # Try multiple approaches to find the result count
    value = None

    # Method 1: Try the meta tag (most reliable)
    meta_content = tree.xpath('//meta[@name="govuk:search-result-count"]/@content')
    if meta_content:
        value = int(meta_content[0])
        logger.info("Found count in meta tag: %d", value)

    # Method 2: Try the span with class js-result-count
    if value is None:
        span_text = tree.xpath('//span[@class="js-result-count"]/text()')
        if span_text:
            # Extract number from text like "96,269 results"
            numbers = re.findall(r"\d+,?\d+", span_text[0])
            if numbers:
                value = int(numbers[0].replace(",", ""))
                logger.info("Found count in span text: %d", value)

    if value is not None:
        dict_data = {"time": strftime("%Y-%m-%d %H:%M:%S"), "count": value}
        logger.info("Successfully found GOV.UK statistics count: %d", value)
        write_json_log(dict_data, log_file=str(config.logfile))

        # Create visualization after updating data
        try:
            create_visualization()
            logger.info("Successfully created visualization")
        except Exception as e:
            logger.error("Failed to create visualization: %s", e)
    else:
        raise ValueError("Could not find result count using any method")

except Exception:
    logger.exception("Error fetching GOV.UK statistics")
