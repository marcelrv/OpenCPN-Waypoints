#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create  bridges layers GPX file for OpenCPN
incl bedieningstijden en marifoonkanalen
@author: Marcel Verpaalen

using https://www.vaarweginformatie.nl/frp/main/#/page/services

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.2"

import datetime
import xml.etree.ElementTree as mod_etree
import requests
from requests.exceptions import HTTPError
import gpxpy
import gpxpy.gpx
import json
import re
import os
import time

baseURL = 'https://www.vaarweginformatie.nl/wfswms/dataservice/1.3/'
workingFolder = './working/'
debugging = False


class BridgeInfo:
    def __init__(self, bridges, operatingtimes, radiocallinpoint):
        self.bridges = bridges
        self.operatingtimes = operatingtimes
        self.radiocallinpoint = radiocallinpoint

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

    def create_bridgeGPX(self, country='NL'):
        # adjust to OpenCPN Scale (at which scale this is visible) disable if not needed
        _UseScale = True
        _ScaleMin = 50000

        gpx = gpxpy.gpx.GPX()
        if isinstance(country, str):
            gpx.name = country + ' Bruggen'
            gpx.description = country + ' bruggeninformatie voor import in OpenCPN downloaded from www.vaarweginformatie.nl'
        else:
            gpx.name = country['name'] + ' Bruggen'
            gpx.description = country['name'] + \
                ' bruggeninformatie voor import in OpenCPN downloaded from www.vaarweginformatie.nl'
        gpx.creator = 'bridges.py -- https://github.com/marcelrv/OpenCPN-Waypoints'
        gpx.author_name = 'Marcel Verpaalen'
        gpx.copyright_year = '2022'
        gpx.copyright_license = 'CC BY-NC-SA 4.0'
        gpx.time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

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

        for bridge in self.bridges:
            gpx_wps = gpxpy.gpx.GPXWaypoint()
            #pnt = bridge["Geometry"].replace("POINT (", "").replace(")", "").split(" ")
            pnt = re.search(r"\((.*)\)", bridge["Geometry"]).group(1).split(" ")
            gpx_wps.longitude = pnt[0]
            gpx_wps.latitude = pnt[1]
            gpx_wps.name = bridge["Name"]
            gpx_wps.link = 'https://vaarweginformatie.nl/frp/main/#/geo/detail/BRIDGE/' + \
                str(bridge["Id"])
            gpx_wps.link_text = bridge["Name"] + ' detail info'
            description = []
            if bridge.get('CanOpen') is True:
                description.append('Type: Bedienbare Brug')
                gpx_wps.symbol = "Landmarks-Bridge2"
            else:
                description.append('Type: Vaste Brug')
                gpx_wps.symbol = "Landmarks-Bridge1"
            radiopoint = self.find_child(self.radiocallinpoint, bridge.get('Id'))
            if radiopoint is not None:
                description.append('VHF:  ' + ','.join(radiopoint.get('VhfChannels')))
            if bridge.get('OperatingTimesId') is not None:
                openingHours = self.get_openingHours(bridge.get('OperatingTimesId'))
                description.append(openingHours)
            gpx_wps.description = '\r\n'.join(description)
            if isinstance(country, str):
                if bridge.get('ForeignCode') == None and country == 'NL':
                    gpx.waypoints.append(gpx_wps)
                elif bridge.get('ForeignCode') is not None:
                    if bridge.get('ForeignCode')[:2] == country:
                        gpx.waypoints.append(gpx_wps)
            else:
                from_Coord = country['from'].split(',')
                to_Coord = country['to'].split(',')
                if float(pnt[1]) > float(from_Coord[0]) and float(pnt[0]) > float(from_Coord[1]) and\
                   float(pnt[1]) < float(to_Coord[0]) and float(pnt[0]) < float(to_Coord[1]):
                    gpx.waypoints.append(gpx_wps)
        return gpx


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
    fn = name + '.gpx'
    f = open(fn, "w")
    f.write(gpx.to_xml())
    f.close()
    print("GPX exported to " + fn)


if __name__ == "__main__":

    response = requests.get(baseURL + 'geogeneration')
    geoInfo = response.json()
    print(f"Latest geoinfomation: {json.dumps(geoInfo,indent=2)}")

#    download all available info instead of required only
#    response = requests.get(baseURL + 'geotype')
#    geotypes = response.json()
#    print ( f"Available geotypes:\r\n {json.dumps(geotypes,indent=2)}")
    geotypes = ['bridge', 'operatingtimes', 'radiocallinpoint']

    for geotype in geotypes:
        fn = workingFolder + geotype + 'Download.json'
        if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > 60*60*24:
            res = download_geo_data(geotype, geoInfo['GeoGeneration'])
            saveJson(fn, res)
        else:
            print(
                f'Reusing existing {fn} which is {int((time.time() -  os.path.getmtime(fn))/3600)} hours old')

    bridges = readJson(workingFolder + 'bridgeDownload.json')
    operatingtimes = readJson(workingFolder + 'operatingtimesDownload.json')
    radiocallinpoint = readJson(workingFolder + 'radiocallinpointDownload.json')

    countries = ['NL']
    for bridge in bridges:
        fc = bridge.get('ForeignCode')
        if fc is not None:
            if fc[:2] not in countries:
                countries.append(fc[:2])
    print(f'Available countries in the database: {countries}')

    bridgeInfo = BridgeInfo(bridges, operatingtimes, radiocallinpoint)
    countries = []
    for country in countries:
        gpx = bridgeInfo.create_bridgeGPX(country)
        gpx.time = datetime.datetime.strptime(geoInfo['PublicationDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if debugging:
            print('Created GPX:', gpx.to_xml())
        saveGPX(gpx, country + "-Bridges")
    #53.120605, 6.318042
    #53.447370, 6.372974
    for region in [{'name': 'Friesland', 'from': '52.774726, 5.340259', 'to': '53.447370, 6.372974'}]:
        gpx = bridgeInfo.create_bridgeGPX(region)
        gpx.time = datetime.datetime.strptime(geoInfo['PublicationDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if debugging:
            print('Created GPX:', gpx.to_xml())
        saveGPX(gpx, region['name'] + "-Bridges")
