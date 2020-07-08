#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create marrekrite GPX file for OpenCPN
@author: Marcel Verpaalen

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2020"
__license__ = "AGPL 3.0"
__version__ = "1.0.1"


import requests
from requests.exceptions import HTTPError
import gpxpy
import gpxpy.gpx

# https://www.marrekrite.frl/wp-json/api/var/get/attributes
# https://www.marrekrite.frl/wp-json/api/wnt/get/lines
# https://www.marrekrite.frl/wp-json/api/fkp/get/lines


gpx = gpxpy.gpx.GPX()
gpx.name = 'Marrekrite aanlegplaatsen'
gpx.description = 'Marrekrite aanlegplaatsen download from https://www.marrekrite.frl'

#for  ty in "top,fkp,wnt,hus,var".split(","):
for  ty in "var".split(","):

    try:
        response = requests.get('https://www.marrekrite.frl/wp-json/api/'+ ty + '/get/points')
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        
        response = requests.get('https://www.marrekrite.frl/wp-json/api/var/get/attributes')
        response.raise_for_status()
        # access JSOn content
        attributes = response.json()

#        print("Entire JSON response for " + ty)
#        print(json.dumps(jsonResponse,indent=2))
        
        for locType in jsonResponse:
#            print(locType, '->', jsonResponse[locType])
            location_group = jsonResponse[locType]
            for point in  location_group["points"]:
                print (point)
                gpx_wps = gpxpy.gpx.GPXWaypoint()
                pnt=point["point"].split(";")[1].replace("POINT(","").replace(")","").split(" ")
                gpx_wps.longitude = pnt[1]
                gpx_wps.latitude= pnt[0]
                if location_group[ "type"]["isBoei"] == 1:
                    gpx_wps.symbol = "Marks-Mooring-Float"
                else:
                       gpx_wps.symbol = "Service-Dock"
                #print (pnt)
                loc_attribute = attributes.get(str(point["id"]))  
                desc =""
                for a in loc_attribute:
                    name = a["name" ]
                    description = str(a["value" ])
                    if a['id'] == 152:
                        gpx_wps.name = ((point["name"] if point["name"] is not None else " " ) + " " + ( description if  description is not None else " " ) ).strip() + " (" + location_group[ "type"]["description"] + ")"
                    desc = desc + name + ' ' * ( 60 - len (name) - len (description) ) + description + '\r\n'
                gpx_wps.description = desc
#                print (loc_attribute)
                gpx.waypoints.append(gpx_wps)
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

print('Created GPX:', gpx.to_xml())
fn = "marrekrite.gpx"
f = open(fn, "w")
f.write( gpx.to_xml())
f.close()
print ("Exported to " + fn)
