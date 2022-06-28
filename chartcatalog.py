#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update chartcatalogs when gpx files are processed and have changes
@author: Marcel Verpaalen

"""
import os
import datetime
import hashlib
import json
from functools import partial
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import jsonpickle

from ChartCatalogs import Chart, RncChartCatalog

working_folder = './working/'
catalog_folder = './chartcatalog/'


def md5sum(filename) -> str:
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()


def md5hash(stringToHash: str) -> str:
    m = hashlib.md5()
    m.update(stringToHash.encode('utf-8'))
    return m.hexdigest()


class ChartInfo:
    def __init__(self, name: str, description: str, source_filename: str, md5: str = '', sort: int = -1,
                 updated=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()):
        self.name: str = name
        self.filename: str = source_filename
        self.md5: str = md5
        self.sort: int = sort
        self.updated: str = updated
        self.description = description

    def get_fileExtension(self):
        return '.%s' % self.filename.split('.')[-1]

    def get_baseFilename(self):
        return ('.').join(self.filename.split('.')[:-1])

    def get_chartFolder_filename(self) -> str:
        zip_name = self.get_baseFilename() + '.zip'
        return catalog_folder + zip_name

    def saveZip(self):
        if self.get_fileExtension() != '.zip':
            zip_name = self.get_chartFolder_filename()
            with ZipFile(zip_name, 'w') as zip:
                zip.write(self.filename)
            print('zipped %s to %s' % (self.filename, zip_name))
        else:
            print('already zip %s' % (self.filename))


class OpenCPNChartCatalog:
    """Create chart catalog file to easy load the files in OpenCPN."""

    def __init__(self):
        self.charts_info_filename = 'chartInfo.json'
        self.charts_info: list[ChartInfo] = jsonpickle.decode(string=Path(
            self.charts_info_filename).read_text(), classes=list[ChartInfo])

    def get_charts(self):
        return self.charts_info

    def get_info(self, filename: str) -> ChartInfo:
        for chartinfo in self.charts_info:
            if chartinfo.filename == filename:
                return chartinfo
        return None

    def store_chartinfo(self):
        frozen = jsonpickle.encode(self.charts_info)
        f = open(self.charts_info_filename, "w")
        f.write(json.dumps(json.loads(frozen), indent=2))
        f.close()

    def isModified(self, filename: str) -> bool:
        chart = self.get_info(filename)
        if chart.get_fileExtension() == '.gpx':
            et = ElementTree.parse(filename)
            root = et.getroot()
            p = root.find('{http://www.topografix.com/GPX/1/1}metadata')
            c = root.find('{http://www.topografix.com/GPX/1/1}metadata/{http://www.topografix.com/GPX/1/1}time')
            if p is not None and c is not None:
                p.remove(c)
            else:
                print('Could not find timestamp in', filename)
            et.write(working_folder + filename)
            md5 = md5sum(filename=working_folder + filename)
        else:
            md5 = md5sum(filename=catalog_folder + filename)
        if md5 == chart.md5:
            print('unchanged', filename, md5, chart.md5)
            chart.md5 = md5
            return False
        print('Changed!', filename, md5, chart.md5)
        chart.md5 = md5
        return True

    def update_chartCatalog(self):
        catalog = RncChartCatalog()
        catalog.title = 'Netherlands Inland & Surroundings GPX waypoints ' + \
            'with buoys, berths, bridges and locks etc. to import as layer (manually).'

        for chart in self.charts_info:
            time = datetime.datetime.fromisoformat(chart.updated)
            if chart.get_fileExtension() == '.gpx':
                fn = chart.get_baseFilename() + '.zip'
            else:
                fn = chart.filename
            self.add_chart(catalog, chart.description, time, fn, chart.sort)
        self.store_catalog(catalog)

    def add_and_store_chart(self, description: str, update_date: datetime, filename: str):
        zip_name = filename + '.zip'
        with ZipFile(catalog_folder + zip_name, 'w') as zip:
            zip.write(filename + '.gpx')
        self.add_chart(description, update_date, zip_name)

    def add_chart(self, catalog, description: str, update_date: datetime, filename: str, number):
        chart = Chart()
        chart.chart_format = 'Sailing Chart, International Chart'
        chart.url = "https://raw.githubusercontent.com/marcelrv/OpenCPN-Waypoints/main/chartcatalog/%s" % (
            filename)
        chart.title = "%s" % description
        chart.number = str(number)
        chart.zipfile_ts = update_date
        chart.target_filename = "%s" % filename
        catalog.add_chart(chart)

    def store_catalog(self, catalog: RncChartCatalog):
        filename = catalog_folder + 'NL-waypoints.xml'
        f = open(filename, "w")
        f.write(catalog.get_xml(True))
        f.close()
        print("Catalog exported to " + filename)


if __name__ == "__main__":

    catalog = OpenCPNChartCatalog()
    hasUpdate = False
    for chart in catalog.get_charts():
        if catalog.isModified(chart.filename):
            chart.saveZip()
            chart.updated = datetime.datetime.fromtimestamp(
                os.path.getmtime(chart.get_chartFolder_filename())).isoformat()
            hasUpdate = True
    if hasUpdate:
        print('Updates,saving catalog files...')
        catalog.update_chartCatalog()
        catalog.store_chartinfo()
    else:
        print('No updates, exit without saving files...')
