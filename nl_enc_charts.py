#!/usr/bin/python
"""Script to process the JSON feed of the Dutch IENC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2019-2023 Marcel Verpaalen
Licensed under GPLv2 or, at your will later version
"""

from ChartCatalogs import Chart, RncChartCatalog
from datetime import datetime
import json
from urllib.request import urlopen 

catalog_folder = './chartcatalog/'


def store_catalog(catalog: RncChartCatalog):
    filename = catalog_folder + 'nl_enc_charts.xml'
    f = open(filename, "w")
    f.write(catalog.get_xml(True))
    f.close()
    print("Catalog exported to " + filename)


catalog = RncChartCatalog()
catalog.title = "Netherlands Inland ENC Charts (daily refresh)"

url = 'https://vaarweginformatie.nl/frp/api/webcontent/downloads?pageId=infra/enc'
with urlopen(url) as f:
    data = json.load(f)
    cnt = 0
    for tileset in data:
        chart = Chart()
        chart.chart_format = 'Sailing Chart, International Chart'
        chart.url = "https://vaarweginformatie.nl/fdd/main/wicket/resource/org.apache.wicket.Application/downloadfileResource?fileId=%s" % tileset['fileId']
        chart.number = "%s" % cnt
        chart.title = "%s" % tileset['name']
        chart.zipfile_ts = datetime.fromtimestamp(tileset['date']/1000)
        chart.target_filename = "%s.zip" % tileset['name']
        try:
            response = urlopen(chart.url)
            filename = response.headers.get_filename()
            if filename is not None:
                chart.target_filename = filename
        except Exception:
            pass
        catalog.add_chart(chart)
        cnt = cnt + 1

store_catalog(catalog)
