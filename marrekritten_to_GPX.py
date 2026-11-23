#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create marrekrite GPX file for OpenCPN
@author: Marcel Verpaalen

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2020 - 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.4"
__updated__ = "2026-11-23"

import datetime
import xml.etree.ElementTree as mod_etree

import gpxpy
import gpxpy.gpx
import sys
import requests

# adjust to OpenCPN Scale (at which scale this is visible) disable if not needed
_UseScale = True
_ScaleMin = 50000

BASE_URL = "https://marrekrite.frl/wp-content/uploads/cache/marrekritekaart"
REQUEST_TIMEOUT = 30

# https://marrekrite.frl/wp-content/uploads/cache/marrekritekaart/var/points.json
# https://marrekrite.frl/wp-content/uploads/cache/marrekritekaart/var/attributes.json
# https://marrekrite.frl/wp-content/uploads/cache/marrekritekaart/wnt/lines.json
# https://marrekrite.frl/wp-content/uploads/cache/marrekritekaart/fkp/lines.json


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
            f'{BASE_URL}/{ty}/points.json', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()

        response = requests.get(
            f'{BASE_URL}/{ty}/attributes.json', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        # access JSON content
        attributes = response.json()
    except (requests.RequestException, ValueError) as err:
        # Keep the published file: a partial download must not replace it
        print(f'::warning::Marrekrite download failed, GPX not updated: {err}')
        sys.exit(0)

#        print("Entire JSON response for " + ty)
#        print(json.dumps(jsonResponse,indent=2))

    skipped = 0
    for locType in jsonResponse:
        #            print(locType, '->', jsonResponse[locType])
        location_group = jsonResponse[locType]
        group_type = location_group["type"]
        is_boei = group_type.get("b", group_type.get("isBoei")) == 1
        type_desc = group_type.get("d", group_type.get("description", ""))
        for point in location_group["points"]:
            print(point)
            try:
                gpx_wps = gpxpy.gpx.GPXWaypoint()
                pnt = point["point"].split(";")[1].replace(
                    "POINT(", "").replace(")", "").split(" ")
                gpx_wps.longitude = pnt[1]
                gpx_wps.latitude = pnt[0]
                if is_boei:
                    gpx_wps.symbol = "Marks-Mooring-Float"
                else:
                    gpx_wps.symbol = "Service-Dock"
                # print (pnt)
                loc_attribute = attributes.get(str(point["id"]))
                if loc_attribute is None:
                    print(f'Warning: no attributes found for point {point["id"]}, skipping.')
                    continue
                desc = ""
                for a in loc_attribute:
                    name = a["name"]
                    description = str(a["value"])
                    if a['id'] == 152:
                        wp_name = ((point["name"] if point["name"] is not None else " ") + " " +
                                   (description if description is not None else " ")).strip() + \
                                   " (" + type_desc + ")"
                        gpx_wps.name = wp_name
                    desc = desc + name + ' ' * \
                        max((33 - len(name) - len(description)), 1) + \
                        description + '\n'  # '<BR>\r'
                gpx_wps.description = desc
#                print (loc_attribute)
                if _UseScale:
                    gpx_wps.extensions.append(root)
                gpx.waypoints.append(gpx_wps)
            except (KeyError, IndexError, TypeError, AttributeError, ValueError) as err:
                # Skip one malformed point instead of dropping all points after it
                skipped += 1
                print(f'::warning::Skipping malformed Marrekrite point {point}: {err!r}')
    if skipped:
        print(f'{skipped} malformed points skipped')

fn = "Marrekrite-Aanlegplaatsen.gpx"
if len(gpx.waypoints) == 0:
    # Do not overwrite the published file with an empty one
    print(f'GPX with 0 waypoints SKIPPED: {fn}')
    sys.exit(0)
print('Created GPX:', gpx.to_xml())
f = open(fn, "w")
f.write(gpx.to_xml())
f.close()
print("Exported to " + fn)
