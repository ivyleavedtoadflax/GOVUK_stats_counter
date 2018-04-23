# coding: utf-8

import requests
from lxml import html
import json
from time import strftime

gov_url = 'https://www.gov.uk/government/statistics'
path = '//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]/text()'
page = requests.get(gov_url)
tree = html.fromstring(page.content)
value = tree.xpath(path)[0]
value = value.replace(',' , '')

value =  "\n%s,%s" % (strftime("%Y-%m-%d %H:%M:%S"), int(value))

log = open("/data/govuk_stats_log.csv", "a")
log.write(value)
log.close()
