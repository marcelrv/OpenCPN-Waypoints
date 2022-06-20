#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create bridges & locks layers GPX file for OpenCPN
incl bedieningstijden en marifoonkanalen
@author: Marcel Verpaalen

using https://www.vaarweginformatie.nl/frp/main/#/page/services

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.2"

import datetime
import json
import os
import re
import time
import xml.etree.ElementTree as mod_etree

import gpxpy
import gpxpy.gpx
import requests
from requests.exceptions import HTTPError
try:
    from ChartCatalogs import Chart, RncChartCatalog
    from zipfile import ZipFile
except ImportError:
    external_module = None

baseURL = 'https://www.vaarweginformatie.nl/wfswms/dataservice/1.3/'
workingFolder = './working/'
debugging = False


class BridgeInfo:
    """Create bridges and locks  waypoints."""

    def __init__(self, bridges, operatingtimes, radiocallinpoint, fairway, related=[]):
        self.bridges = bridges
        self.operatingtimes = operatingtimes
        self.radiocallinpoint = radiocallinpoint
        self.fairway = fairway
        self.related = related

    def find_related(self, data, related_data, id_type: str):
        id = data.get(id_type)
        related_data_type = id_type[:-2]
        if id is not None:
            for related in related_data:
                if related[related_data_type] is not None:
                    for rec in related[related_data_type]:
                        if rec.get('Id') == id:
                            return rec
        return None

    def find_id(self, data, id):
        for rec in data:
            if rec.get('Id') == id:
                return rec

    def find_child(self, data, id):
        for rec in data:
            if rec.get('ParentId') == id:
                return rec

    def operatinghours_sort_key(self, operatingRule):
        t = operatingRule.get('From')
        if t is not None:
            if operatingRule.get('IsMonday'):
                t -= 3
            if operatingRule.get('IsSaturday'):
                t += 1
            if operatingRule.get('IsSunday'):
                t += 2
            return operatingRule.get('From')
        return 9999900000

    def get_openingHours(self, openingId):
        openings = self.find_id(self.operatingtimes, openingId)
        openingDescription = '\r\nBedieningstijden\r\n'
        for OperatingPeriod in openings.get('OperatingPeriods'):
            openingDescription += 'Periode ' + OperatingPeriod['Start'][2:] + '-' + OperatingPeriod['Start'][:2] + \
                ' tot ' + OperatingPeriod['End'][2:] + '-' + OperatingPeriod['End'][:2] + ':\r\n'
            for OperatingRule in sorted(OperatingPeriod['OperatingRules'], key=self.operatinghours_sort_key):
                if OperatingRule.get('From') is not None and OperatingRule.get('To') is not None and OperatingRule.get('From') > 0:
                    openingDescription += '   ' + datetime.datetime.fromtimestamp(OperatingRule['From'] / 1000.0).strftime(
                        '%H:%M') + ' - ' + datetime.datetime.fromtimestamp(OperatingRule['To'] / 1000.0).strftime('%H:%M') + ': '
                else:
                    openingDescription += '   Gesloten: '
                if OperatingRule.get('IsMonday'):
                    openingDescription += 'Ma, '
                if OperatingRule.get('IsTuesday'):
                    openingDescription += 'Di, '
                if OperatingRule.get('IsWednesday'):
                    openingDescription += 'Wo, '
                if OperatingRule.get('IsThursday'):
                    openingDescription += 'Do, '
                if OperatingRule.get('IsFriday'):
                    openingDescription += 'Vr, '
                if OperatingRule.get('IsSaturday'):
                    openingDescription += 'Za, '
                if OperatingRule.get('IsSunday'):
                    openingDescription += 'Zo, '
                if OperatingRule.get('IsHoliday'):
                    openingDescription += 'incl. feestdagen.\r\n'
                else:
                    openingDescription += 'excl. feestdagen.\r\n'
        if openings.get('Note') is not None:
            openingDescription += '\r\nNote: ' + openings.get('Note')
        return openingDescription

    def create_header(self, region, geotype):
        gpx = create_GPXheader()
        description = region['name']
        if geotype == 'lock':
            gpx.name = region['name'] + ' Sluizen'
            description += ' sluis informatie'
        elif geotype == 'vinharbour':
            gpx.name = region['name'] + ' Jachthavens'
            description += ' jachthaven informatie'
        else:
            gpx.name = region['name'] + ' Bruggen'
            description += ' bruggeninformatie'
        if region.get('country') is None or region.get('country') == 'NL':
            description += ' incl. openings tijden'
        gpx.description = description + ' based on RWS information'
        return gpx

    def create_bridgeGPX(self, region, geotype):

        # adjust to OpenCPN Scale (at which scale this is visible) disable if not needed
        _UseScale = True
        _ScaleMin = 160000

        gpx = self.create_header(region, geotype)
        if _UseScale:
            root = create_GPX_namespace(gpx, _ScaleMin)

        for bridge in self.bridges:
            gpx_wps = gpxpy.gpx.GPXWaypoint()
            #pnt = bridge["Geometry"].replace("POINT (", "").replace(")", "").split(" ")
            pnt = re.search(r"\((.*)\)", bridge["Geometry"]).group(1)
            pnt = pnt.split(',')[0].split(" ")
            gpx_wps.longitude = pnt[0]
            gpx_wps.latitude = pnt[1]
            name = bridge["Name"]
            radio_record = bridge
            if _UseScale:
                gpx_wps.extensions.append(root)
            description = []
            fairway_id = bridge.get('FairwayId')
            if fairway_id is not None:
                fairway = self.find_id(self.fairway, fairway_id)
                if fairway is not None:
                    description.append('Locatie: %s' % fairway.get('Name'))
            if geotype == 'lock':
                gpx_wps.symbol = "Symbol-Spot-Magenta"
            elif 'harbour' in geotype:
                vinHarbour = self.find_related(bridge, self.related, 'VinHarbourId')
                if vinHarbour is not None:
                    name = vinHarbour["Name"]
                    radio_record = vinHarbour
                    if vinHarbour.get('Note') is not None:
                        description.append('Opmerking      : %s' % vinHarbour.get('Note'))
                gpx_wps.symbol = "Anchor"
                short_stay_places = bridge.get('ShortStayPlaces')
                if (short_stay_places) is not None:
                    description.append('Passanten plaatsen: %d' % short_stay_places)
                long_stay_places = bridge.get('LongStayPlaces')
                if (long_stay_places) is not None:
                    description.append('Vaste ligplaatsen: %d' % long_stay_places)
                if bridge.get('SuppliesFuel') is True:
                    description.append('Tankstation:      : Ja')
                else:
                    description.append('Tankstation:      : Nee')
            elif geotype == 'bridge':
                if bridge.get('CanOpen') is True:
                    description.append('Type:    Bedienbare Brug')
                    gpx_wps.symbol = "Landmarks-Bridge2"
                else:
                    description.append('Type:    Vaste Brug')
                    gpx_wps.symbol = "Landmarks-Bridge1"
            else:
                gpx_wps.symbol = "Circle"
            radiopoint = self.find_child(self.radiocallinpoint, radio_record.get('Id'))
            if radiopoint is not None:
                description.append('VHF:     ' + ','.join(radiopoint.get('VhfChannels')))
            if bridge.get('OperatingTimesId') is not None:
                openingHours = self.get_openingHours(bridge.get('OperatingTimesId'))
                description.append(openingHours)
            link_type = str(bridge['GeoType']).upper()
            if 'HARBOUR' in link_type:
                link_type = 'shipstation'
            gpx_wps.link = 'https://vaarweginformatie.nl/frp/main/#/geo/detail/' + link_type + '/' + \
                str(bridge["Id"])
            gpx_wps.link_text = name + ' online info'
            gpx_wps.name = name
            gpx_wps.description = '\r\n'.join(description)
            country = region.get('country')
            foreign_code = bridge.get('ForeignCode')
            if foreign_code is not None:
                foreign_code = foreign_code[:2]
                if foreign_code == '65':  # hack as no country
                    foreign_code = 'BE'
            else:
                foreign_code = 'NL'
            if country is not None:
                if country == foreign_code:
                    gpx.waypoints.append(gpx_wps)
            else:
                from_Coord = region['from']
                to_Coord = region['to']
                if float(pnt[1]) > from_Coord[0] and float(pnt[0]) > from_Coord[1] and\
                   float(pnt[1]) < to_Coord[0] and float(pnt[0]) < to_Coord[1]:
                    gpx.waypoints.append(gpx_wps)
        return gpx


class RadioInfo:
    """Create VHF radion station waypoints."""

    def __init__(self,  radiocallinpoint):
        self.radiocallinpoint = radiocallinpoint

    def create_radioGPX(self, region, channelVHFonly=True):
        _UseScale = True
        _ScaleMin = 100000

        gpx = create_GPXheader()
        if _UseScale:
            root = create_GPX_namespace(gpx, _ScaleMin)

        gpx.name = region['name'] + ' Marifoon meldpunten'
        description = region['name'] + ' Marifoon meldpunten'
        if channelVHFonly:
            description += ' with VHF channel in name'
        gpx.description = description + ' based on RWS data'

        for radio in self.radiocallinpoint:
            gpx_wps = gpxpy.gpx.GPXWaypoint()
            pnt = re.search(r"\((.*)\)", radio["Geometry"]).group(1).split(" ")
            gpx_wps.longitude = pnt[0]
            gpx_wps.latitude = pnt[1]
            if channelVHFonly:
                gpx_wps.name = 'VHF ' + ','.join(radio.get('VhfChannels'))
            else:
                gpx_wps.name = radio["Name"]
            gpx_wps.link = 'https://vaarweginformatie.nl/frp/main/#/geo/detail/' + radio.get('ParentGeoType').upper() + '/' + \
                str(radio['ParentId'])
            gpx_wps.link_text = radio["Name"] + ' online info'
            if _UseScale:
                gpx_wps.extensions.append(root)
            description = []
            gpx_wps.symbol = "Info-Info"
            description.append('Naam:         ' + radio["Name"])
            description.append('VHF:          ' + ','.join(radio.get('VhfChannels')))
            if radio.get('RadioStatus') is not None:
                description.append('RadioStatus: ' + radio['RadioStatus'])
                gpx_wps.symbol = "Symbol-Exclamation-Blue"
            description.append('RadioTraffic: ' + radio.get('RadioTraffic'))
            gpx_wps.description = '\r\n'.join(description)
            country = region.get('country')
            foreign_code = radio.get('ForeignCode')
            if foreign_code is not None:
                foreign_code = foreign_code[:2]
                if foreign_code == '65':  # hack as no country
                    foreign_code = 'BE'
            else:
                foreign_code = 'NL'
            if country is not None:
                if country == foreign_code:
                    gpx.waypoints.append(gpx_wps)
            else:
                from_Coord = region['from']
                to_Coord = region['to']
                if float(pnt[1]) > from_Coord[0] and float(pnt[0]) > from_Coord[1] and\
                   float(pnt[1]) < to_Coord[0] and float(pnt[0]) < to_Coord[1]:
                    gpx.waypoints.append(gpx_wps)
        return gpx


class OpenCPNChartCatalog:
    """Create chart catalog file to easy load the files in OpenCPN."""

    def __init__(self):
        self.catalog = RncChartCatalog()
        self.catalog.title = 'Netherlands Inland & Surroundings GPX waypoints ' + \
            'with  berths, bridges and locks etc. to import as layer (manually).'
        self.counter = 0
        self.catalog_folder = 'chartcatalog/'
        # add other files
        self.add_and_store_chart('Marrekrite aanleg plaatsen', datetime.datetime.fromtimestamp(
            os.path.getmtime('marrekrite.gpx')), 'marrekrite')

    def add_and_store_chart(self, description: str,  update_date: datetime, filename: str):
        zip_name = filename + '.zip'
        with ZipFile(self.catalog_folder + zip_name, 'w') as zip:
            zip.write(filename + '.gpx')
        self.add_chart(description, update_date, zip_name)

    def add_chart(self, description: str,  update_date: datetime, filename: str):
        chart = Chart()
        chart.chart_format = 'Sailing Chart, International Chart'
        chart.url = "https://raw.githubusercontent.com/marcelrv/OpenCPN-Waypoints/master/%s" % self.catalog_folder + filename
        chart.number = "%s" % self.counter
        chart.title = "%s" % description
        chart.zipfile_ts = update_date
        chart.target_filename = "%s" % filename
        self.catalog.add_chart(chart)
        self.counter += 1

    def store_catalog(self):
        filename = self.catalog_folder+'NL-waypoints.xml'
        f = open(filename, "w")
        f.write(self.catalog.get_xml(True))
        f.close()
        print("Catalog exported to " + filename)


def create_GPXheader():
    gpx = gpxpy.gpx.GPX()
    gpx.creator = 'vwi_waypoints_generator.py -- https://github.com/marcelrv/OpenCPN-Waypoints'
    gpx.author_name = 'Marcel Verpaalen'
    gpx.copyright_year = '2022'
    gpx.copyright_license = 'CC BY-NC-SA 4.0'
    gpx.time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return gpx


def create_GPX_namespace(gpx, ScaleMin):
    # adjust to OpenCPN Scale (at which scale this is visible) disable if not needed
    _UseScale = True
    _ScaleMin = ScaleMin

    # definition of extension
    namespace = '{opencpn}'

    # create extension element
    root = mod_etree.Element(namespace + 'scale_min_max')
    root.attrib['UseScale'] = str(_UseScale)
    root.attrib['ScaleMin'] = str(_ScaleMin)
    root.attrib['ScaleMax'] = "0"

    # add extension to header
    if _UseScale:
        nsmap = {namespace[1:-1]: 'http://www.opencpn.org'}
        gpx.nsmap = nsmap
    return root


def download_geo_data(geotype, geogeneration):
    download_done = False
    result = []
    counter = 0
    while not download_done:
        try:
            url = baseURL + str(geogeneration) + '/' + geotype + \
                '?offset=' + str(counter) + '&count=100'
            response = requests.get(url)
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()

            if debugging:
                print("Downloading JSON response for " + url)
                print(json.dumps(jsonResponse, indent=2))

            result.extend(jsonResponse['Result'])
            print(f"Processed {counter} of {str(jsonResponse['TotalCount'])} from {url}")
            counter = counter + jsonResponse['Count']
            if (counter >= jsonResponse['TotalCount']):
                download_done = True

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            download_done = True
        except Exception as err:
            print(f'Other error occurred: {err}')
            download_done = True
    return result


def saveJson(filename, data):
    f = open(filename, "w")
    f.write(json.dumps(data, indent=2))
    f.close()
    print("Exported to " + filename)


def readJson(filename):
    with open(filename) as f:
        return json.load(f)


def saveGPX(gpx, name):
    if debugging:
        print('Created GPX:', gpx.to_xml())
    waypoints = len(gpx.waypoints)
    if waypoints == 0:
        print(f'GPX with {str(waypoints)} waypoints SKIPPED: {name}')
        return
    fn = name + '.gpx'
    f = open(fn, "w")
    f.write(gpx.to_xml())
    f.close()
    print(f'GPX with {str(waypoints)} points exported to {fn}')


def saveGPX_and_catalog(gpx, name: str, description: str, publication_date: datetime):
    waypoints = len(gpx.waypoints)
    if waypoints == 0:
        print(f'GPX with {str(waypoints)} waypoints SKIPPED: {name}')
        return
    saveGPX(gpx, name)
    chart_catalog.add_and_store_chart(description + ' (%d wpts)' %
                                      waypoints, publication_date, name)


if __name__ == "__main__":

    response = requests.get(baseURL + 'geogeneration')
    geoInfo = response.json()
    print(f"Latest geoinfomation: {json.dumps(geoInfo,indent=2)}")
    publication_date = datetime.datetime.strptime(
        geoInfo['PublicationDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    chart_catalog = OpenCPNChartCatalog()
#    download all available info instead of required only
    response = requests.get(baseURL + 'geotype')
    geotypes = response.json()
    print(f"Available geotypes:\r\n {json.dumps(geotypes,indent=2)}")
    # comment below line to download all geotypes
    geotypes = ['bridge', 'operatingtimes', 'radiocallinpoint', 'lock', 'fairway']

    for geotype in geotypes:
        fn = workingFolder + geotype + 'Download.json'
        if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > 60*60*24:
            res = download_geo_data(geotype, geoInfo['GeoGeneration'])
            saveJson(fn, res)
        else:
            print(
                f'Reusing existing {fn} which is {int((time.time() -  os.path.getmtime(fn))/3600)} hours old')

#    isrs = readJson(workingFolder + 'isrsDownload.json')
    bridges = readJson(workingFolder + 'bridgeDownload.json')
    locks = readJson(workingFolder + 'lockDownload.json')
    operatingtimes = readJson(workingFolder + 'operatingtimesDownload.json')
    radiocallinpoint = readJson(workingFolder + 'radiocallinpointDownload.json')
    fairway = readJson(workingFolder + 'fairwayDownload.json')
    vinharbour = readJson(workingFolder + 'vinharbourDownload.json')
    touristharbour = readJson(workingFolder + 'touristharbourDownload.json')

    countries = ['NL']
    for bridge in bridges:
        fc = bridge.get('ForeignCode')
        if fc is not None:
            if fc[:2] not in countries:
                countries.append(fc[:2])
    print(f'Available countries in the database: {countries}')

    # create precooked regions and add an entry for each country found.
    regions = [{'name': 'Friesland', 'from': [52.774726, 5.340259], 'to': [53.447370, 6.372974]}]
    for country in countries:
        regions.append({'name': country, 'country': country})

    # create bridge files
    bridgeInfo = BridgeInfo(bridges, operatingtimes, radiocallinpoint, fairway)
    for region in regions:
        gpx = bridgeInfo.create_bridgeGPX(region, 'bridge')
        gpx.time = publication_date
        name = region['name'] + "-Bruggen"
        saveGPX_and_catalog(gpx, name, gpx.description, publication_date)

    # create locks files
    bridgeInfo = BridgeInfo(locks, operatingtimes, radiocallinpoint, fairway)
    for region in regions:
        gpx = bridgeInfo.create_bridgeGPX(region, 'lock')
        gpx.time = publication_date
        name = region['name'] + "-Sluizen"
        saveGPX_and_catalog(gpx, name, gpx.description, publication_date)

    # create harbours files (vinharbour)
    bridgeInfo = BridgeInfo(touristharbour, operatingtimes, radiocallinpoint,
                            fairway, [{'VinHarbour': vinharbour}])
    for region in regions:
        gpx = bridgeInfo.create_bridgeGPX(region, 'touristharbour')
        gpx.time = publication_date
        name = region['name'] + "-Jachthavens"
        saveGPX_and_catalog(gpx, name, gpx.description, publication_date)

    # create radio VHF files
    radioInfo = RadioInfo(radiocallinpoint)
    gt = []
    for r in radiocallinpoint:
        ParentGeoType = r.get('ParentGeoType')
        if ParentGeoType not in gt:
            gt.append(ParentGeoType)
    print('types in radio:', gt)

    for region in regions:
        gpx = radioInfo.create_radioGPX(region,  channelVHFonly=True)
        gpx.time = publication_date
        name = region['name'] + "-MarifoonPunten-VHFinName"
        saveGPX_and_catalog(gpx, name, gpx.description, publication_date)

        gpx = radioInfo.create_radioGPX(region,  channelVHFonly=False)
        gpx.time = publication_date
        name = region['name'] + "-MarifoonPunten"
        saveGPX_and_catalog(gpx, name, gpx.description, publication_date)

    chart_catalog.store_catalog()
