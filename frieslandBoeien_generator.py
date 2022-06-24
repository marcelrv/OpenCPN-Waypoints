#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Boeien voor Friesland als GPX file for OpenCPN
Sourcedata is geoportaal friesland

@author: Marcel Verpaalen

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.0"

import datetime
import errno
import json
import os
import sys
import re
import time
import xml.etree.ElementTree as mod_etree
from pathlib import Path

import gpxpy
import gpxpy.gpx
import requests
from osgeo import ogr
from osgeo.osr import SpatialReference, CoordinateTransformation, OAMS_TRADITIONAL_GIS_ORDER

workingFolder = './working/'
input_filename = workingFolder + 'frieslandboeien.gml'
outputFileName = 'Frieslandboeien.gpx'
debugging = False
max_age = 60 * 60 * 24  # 24h

# mapping Vaarwegmarkeringen feature naam naar GPX field
mapping = dict([('NAAM', {'dst': 'name', 'isDescription': False}),
                ('TYPE_OMSCHRIJVING', {'dst': 'sym', 'isDescription': True}),
                ('REGLEMENT_VAARWEGNAAM', {'dst': 'vaarweg', 'isDescription': True}),
                ('OPMERKING', {'dst': 'opmerking', 'isDescription': True}),
                ('MODEL', {'dst': 'model', 'isDescription': True}),
                ('MEER', {'dst': 'meer', 'isDescription': True})
                ])
# Mapping van boei type naar icon (nautin usericons)
# note: dit kan misschien nog verbeterd worden met ook het model mee te nemen. De conversie van model naar type boei is mij nog niet helemaal duidelijk

symb = dict([
            ('groene boei', '1041'),
            ('groene boei met topteken', '1003'),
            ('groene lichtboei', '1005'),
            ('groene lichtopstand', '1008'),
            ('groene boei met radarscherm', '1003'),
            ('landbaken groen', '10121'),
            ('landbaken rood', '10111'),
            ('rode boei', '1141'),
            ('rode boei met radarscherm', '1103'),
            ('rode lichtboei', '1105'),
            ('rode lichtopstand', '1108'),
            ('aanvullende markering groen-wit', '1512'),
            ('aanvullende markering rood-wit', '1562'),
            ('bijzondere markering', '3001'),
            ('scheidingsboei gelijke vaarwaters', '1411'),
            ('scheidingsboei groen-rood', '1201'),
            ('scheidingsboei rood-groen', '1251'),
            ('noord cardinaal boei', 'Marks-Cardinal-North'),
            ('oost cardinaal boei', 'Marks-Cardinal-East'),
            ('west cardinaal boei', 'Marks-Cardinal-West'),
            ('zuid cardinaal boei', 'Marks-Cardinal-South'),
            ])
missing = []


def process_gml(input_filename, outName):
    # Define the  projection system (EPSG 28992) sourcedata
    epsg28992 = SpatialReference()
    epsg28992.ImportFromEPSG(28992)

    # Define the wgs84 system (EPSG 4326)
    epsg4326 = SpatialReference()
    epsg4326.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)
    epsg4326.ImportFromEPSG(4326)
    poCT = CoordinateTransformation(epsg28992, epsg4326)

    outDriver = ogr.GetDriverByName('GPX')
    co_opts = ['GPX_USE_EXTENSIONS=yes', 'GPX_EXTENSIONS_NS="{opencpn}"']
    outDataSource = outDriver.CreateDataSource(outName, options=co_opts)
    outLayer = outDataSource.CreateLayer('waypoints', epsg4326, geom_type=ogr.wkbPoint)
    featureDefn = outLayer.GetLayerDefn()

    reader = ogr.Open(input_filename, update=0)

    layer = reader.GetLayer()

    print("GetLayerCount() = %d\n", reader.GetLayerCount())
    for iLayer in range(reader.GetLayerCount()):
        poLayer = reader.GetLayer(iLayer)
        # poLayer.SetSpatialFilter(epsg28992)

        line = "Layer %d: %s" % (iLayer + 1, poLayer.GetLayerDefn().GetName())
        print(line)

        line = "geocount %d: %s" % (iLayer + 1, poLayer.GetLayerDefn().GetGeomFieldCount())

        nGeomFieldCount = poLayer.GetLayerDefn().GetGeomFieldCount()
        if nGeomFieldCount > 0:
            line = line + " ("
            for iGeom in range(nGeomFieldCount):
                if iGeom > 0:
                    line = line + ", "
                poGFldDefn = poLayer.GetLayerDefn().GetGeomFieldDefn(iGeom)
                line = line + "%s" % ogr.GeometryTypeToName(poGFldDefn.GetType())
            line = line + ")"

        if poLayer.GetLayerDefn().GetGeomType() != ogr.wkbUnknown:
            line = line + " (%s)" % ogr.GeometryTypeToName(poLayer.GetLayerDefn().GetGeomType())

        print(line)

        poFeature = poLayer.GetNextFeature()
        while poFeature is not None:
            poDefn = poFeature.GetDefnRef()
            print("OGRFeature(%s):%ld" % (poDefn.GetName(), poFeature.GetFID()))
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetFrom(poFeature)

            poDstGeometry = outFeature.GetGeometryRef()
            if poDstGeometry is not None:
                print('geometry input:       ', poDstGeometry)
                if poCT is not None:
                    eErr = poDstGeometry.Transform(poCT)
                    print('geometry converted:   ', poDstGeometry)
                    if eErr != 0:
                        print("Failed to reproject feature %d (geometry probably out of source or destination SRS)." %
                              poFeature.GetFID())

            description = []

            for iField in range(poDefn.GetFieldCount()):
                poFDefn = poDefn.GetFieldDefn(iField)
                line = "  %s (%s) = " % (poFDefn.GetNameRef(), ogr.GetFieldTypeName(poFDefn.GetType()))
                if poFeature.IsFieldSet(iField) and poFDefn.GetNameRef() in mapping:
                    try:
                        line = line + "%s" % (poFeature.GetFieldAsString(iField))
                        map = mapping[poFDefn.GetNameRef()]
                        value = poFeature.GetFieldAsString(iField)

                        if map['dst'] == 'sym':
                         #   if value[4:] == 'NABO':
                         #       outFeature.SetField(map['dst'], str(value[:-3]))

                            if value in symb:
                                outFeature.SetField(map['dst'], str(symb[value]))
                            else:
                                outFeature.SetField(map['dst'], poFeature.GetFieldAsString(iField))
                                if value not in missing:
                                    missing.append(value)

                        if map['isDescription']:
                            if len(value) > 0:
                                description.append('%s : %s' % (map['dst'], poFeature.GetFieldAsString(iField)))
                        else:
                            outFeature.SetField(map['dst'], poFeature.GetFieldAsString(iField))
                    except:
                        # For Python3 on non-UTF8 strings
                        print('pynonUT', errno)
                        # exit()
                        line = line + "%s" % (poFeature.GetFieldAsBinary(iField))
                else:
                    line = line + "(null)"
                if debugging:
                    print(line)

            if len(description) > 0:
                outFeature.SetField('desc', '\n'.join(description))
            outLayer.CreateFeature(outFeature)
            # dereference the feature
            outFeature = None

            poFeature = poLayer.GetNextFeature()
    reader.Destroy()
    outDataSource.Destroy()


def create_GPXheader(gpx):

    gpx.creator = 'frieslandboeien_generator.py -- https://github.com/marcelrv/OpenCPN-Waypoints'
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


def safeFile(filename, indata):
    f = open(filename, "w", encoding='utf-8')
    f.write(indata)
    f.close()
    print("Exported to " + filename)


def update_source_data(fn):
    if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > 60*60*24:
        print('Downloading %s' % fn)
        url = 'https://geoportaal.fryslan.nl/arcgis/services/ProvinciaalGeoRegister/PGR2/MapServer/wfsServer?request=GetFeature&service=WFS&version=1.1.0&outputFormat=GML3&typeName=Vaarwegmarkeringen'
        response = requests.get(url)
        data = response.text
        safeFile(fn, data)
    else:
        print(
            f'Reusing existing {fn} which is {int((time.time() -  os.path.getmtime(fn))/3600)} hours old')


def saveGPX(gpx, fn):
    if debugging:
        print('Created GPX:', gpx.to_xml())
    waypoints = len(gpx.waypoints)
    if waypoints == 0:
        print(f'GPX with {str(waypoints)} waypoints SKIPPED: {name}')
        return
    f = open(fn, "w")
    f.write(gpx.to_xml())
    f.close()
    print(f'GPX with {str(waypoints)} points exported to {fn}')


if __name__ == "__main__":
    _UseScale = True
    _ScaleMin = 100000

    update_source_data(input_filename)
    process_gml(input_filename, outputFileName)

    # post processing as it is unclear how to do in with gdal
    gpx_file = open(outputFileName, 'r')
    gpx = gpxpy.parse(gpx_file)
    create_GPXheader(gpx)
    if _UseScale:
        root = create_GPX_namespace(gpx, _ScaleMin)
        for gpx_wps in gpx.waypoints:
            gpx_wps.extensions.append(root)
    saveGPX(gpx, outputFileName)

    if len(missing) > 0:
        print('TYPE_OMSCHRIJVING missing in the mapping:')
        for m in sorted(missing):
            print("('%s' , '0')," % m)
