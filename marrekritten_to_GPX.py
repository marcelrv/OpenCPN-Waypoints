#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create marrekrite GPX file for OpenCPN
@author: Marcel Verpaalen

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2020 - 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.2"

import datetime
import xml.etree.ElementTree as mod_etree

import gpxpy
import gpxpy.gpx
import requests
from requests.exceptions import HTTPError

# adjust to OpenCPN Scale (at which scale this is visible) disable if not needed
_UseScale = True
_ScaleMin = 50000

# https://www.marrekrite.frl/wp-json/api/var/get/attributes
# https://www.marrekrite.frl/wp-json/api/wnt/get/lines
# https://www.marrekrite.frl/wp-json/api/fkp/get/lines


gpx = gpxpy.gpx.GPX()
gpx.name = 'Marrekrite aanlegplaatsen'
gpx.creator = 'marrekritten_to_GPX.py -- https://github.com/marcelrv/OpenCPN-Waypoints'
gpx.description = 'Marrekrite aanlegplaatsen download from https://www.marrekrite.frl'
gpx.author_name = 'Marcel Verpaalen'
gpx.copyright_year = '2022'
gpx.copyright_license = 'CC BY-NC-SA 4.0'
 
gpx.time = datetime.datetime.now(datetime.UTC).replace(tzinfo=datetime.timezone.utc)

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

# for  ty in "top,fkp,wnt,hus,var".split(","):
for ty in "var".split(","):
    try:
        response = requests.get(
            'https://marrekrite.frl/wp-json/api/' + ty + '/get/points')
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()

        response = requests.get(
            'https://marrekrite.frl/wp-json/api/var/get/attributes')
        response.raise_for_status()
        # access JSOn content
        attributes = response.json()

#        print("Entire JSON response for " + ty)
#        print(json.dumps(jsonResponse,indent=2))

        for locType in jsonResponse:
            #            print(locType, '->', jsonResponse[locType])
            location_group = jsonResponse[locType]
            for point in location_group["points"]:
                print(point)
                gpx_wps = gpxpy.gpx.GPXWaypoint()
                pnt = point["point"].split(";")[1].replace(
                    "POINT(", "").replace(")", "").split(" ")
                gpx_wps.longitude = pnt[1]
                gpx_wps.latitude = pnt[0]
                if location_group["type"]["isBoei"] == 1:
                    gpx_wps.symbol = "Marks-Mooring-Float"
                else:
                    gpx_wps.symbol = "Service-Dock"
                # print (pnt)
                loc_attribute = attributes.get(str(point["id"]))
                desc = ""
                for a in loc_attribute:
                    name = a["name"]
                    description = str(a["value"])
                    if a['id'] == 152:
                        wp_name = ((point["name"] if point["name"] is not None else " ") + " " +
                                   (description if description is not None else " ")).strip() + \
                                   " (" + location_group["type"]["description"] + ")"
                        gpx_wps.name = wp_name
                    desc = desc + name + ' ' * \
                        max((33 - len(name) - len(description)), 1) + \
                        description + '\n'  # '<BR>\r'
                gpx_wps.description = desc
#                print (loc_attribute)
                if _UseScale:
                    gpx_wps.extensions.append(root)
                gpx.waypoints.append(gpx_wps)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

print('Created GPX:', gpx.to_xml())
fn = "Marrekrite-Aanlegplaatsen.gpx"
f = open(fn, "w")
f.write(gpx.to_xml())
f.close()
print("Exported to " + fn)
