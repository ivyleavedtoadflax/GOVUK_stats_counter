# coding: utf-8

"""
GOV.UK statistics count go getter

Scrape the statistics count from the GOV.UK statistics homepage and 
log it to json for reading by telegraf.
"""

import os
from time import strftime
from lxml import html
import requests
from write_json_log import write_json_log

LOGFILE = os.environ.get('LOGFILE')

gov_url = 'https://www.gov.uk/government/statistics'
path = '//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]/text()'
page = requests.get(gov_url)
tree = html.fromstring(page.content)
value = tree.xpath(path)[0]
value = value.replace(',' , '')

dict_data = {
    'time' : strftime("%Y-%m-%d %H:%M:%S"),
    'count' : int(value)
}

write_json_log(dict_data, log_file=LOGFILE)
