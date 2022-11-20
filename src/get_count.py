# coding: utf-8
"""
GOV.UK statistics count go getter

Scrape the statistics count from the GOV.UK statistics homepage and
log it to json for reading by telegraf.
"""
import os
import re
from logging import getLogger
from time import strftime

import requests
from lxml import html

from write_json_log import write_json_log

logger = getLogger(__name__)

LOGFILE = os.environ.get("LOGFILE")

GOV_URL = "https://www.gov.uk/search/research-and-statistics"
PATH = '//*[(@id = "js-result-count")]/text()'
try:
    page = requests.get(GOV_URL, timeout=5)
    tree = html.fromstring(page.content)
    value = tree.xpath(PATH)[0]
    value = re.findall(r"\d+\,\d+", value)[0]
    value = int(value.replace(",", ""))
    dict_data = {"time": strftime("%Y-%m-%d %H:%M:%S"), "count": int(value)}
    logger.info("GOV.UK statistics value found")
    write_json_log(dict_data, log_file=LOGFILE)
    page.raise_for_status()
except Exception:
    logger.exception("Error fetching GOV.UK statistics")
