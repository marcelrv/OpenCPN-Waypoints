#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Boeien voor Nederland, Friesland als GPX file for OpenCPN
Sourcedata is geoportaal friesland & RWS

@author: Marcel Verpaalen

"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.1"

import errno
import os
import time
import xml.etree.ElementTree as mod_etree

import gpxpy
import gpxpy.gpx
import requests
from osgeo import ogr
from osgeo.osr import SpatialReference, CoordinateTransformation, OAMS_TRADITIONAL_GIS_ORDER

from boeien_gen_def import BoeienSource, nederland, friesland

workingFolder = './working/'
debugging = False
max_age = 60 * 60 * 24  # 24h

missing = []
all_icons_allFiles ={}


def process_gml(input_filename, outName, field_mapping, icon_mapping, epsg=None):
    all_icons = set()

    if epsg is not None:
        # Define the  projection system (EPSG 28992) sourcedata
        source_epsg = SpatialReference()
        source_epsg.ImportFromEPSG(epsg)
    else:
        source_epsg = SpatialReference()
        source_epsg.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)
        source_epsg.ImportFromEPSG(4326)

    # Define the wgs84 system (EPSG 4326)
    epsg4326 = SpatialReference()
    epsg4326.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)
    epsg4326.ImportFromEPSG(4326)

    outDriver = ogr.GetDriverByName('GPX')
    co_opts = ['GPX_USE_EXTENSIONS=yes', 'GPX_EXTENSIONS_NS="{opencpn}"']
    outDataSource = outDriver.CreateDataSource(outName, options=co_opts)
    outLayer = outDataSource.CreateLayer('waypoints', epsg4326, geom_type=ogr.wkbPoint)
    featureDefn = outLayer.GetLayerDefn()

    reader = ogr.Open(input_filename, update=0)

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
            print("OGRFeature (%s): %ld" % (poDefn.GetName(), poFeature.GetFID()))
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetFrom(poFeature)
            poDstGeometry: ogr.Geometry = outFeature.GetGeometryRef()
            if poDstGeometry is not None:
                print('Geometry input:       ', poDstGeometry)
                srsReference: SpatialReference = poDstGeometry.GetSpatialReference()
                if srsReference is None:
                    srsReference = source_epsg
                    print('no SpatialReference, using default')
                poCT = CoordinateTransformation(srsReference, epsg4326)
                if poCT is not None:
                    eErr = poDstGeometry.Transform(poCT)
                    print('Geometry converted:   ', poDstGeometry)
                    if eErr != 0:
                        print("Failed to reproject feature %d (geometry probably out of source or destination SRS)." %
                              poFeature.GetFID())

            description = []
            has_S57sym = False

            for iField in range(poDefn.GetFieldCount()):
                poFDefn = poDefn.GetFieldDefn(iField)
                line = "  %s (%s) = " % (poFDefn.GetNameRef(), ogr.GetFieldTypeName(poFDefn.GetType()))
                if poFeature.IsFieldSet(iField) and poFDefn.GetNameRef().upper() in field_mapping:
                    try:
                        line = line + "%s" % (poFeature.GetFieldAsString(iField))
                        map = field_mapping[poFDefn.GetNameRef().upper()]
                        value = poFeature.GetFieldAsString(iField)

                        if map['isDescription']:
                            if len(value) > 0 and value != 'Niet toegewezen' and value != '#':
                                description.append('%s : %s' % (map['dst'], poFeature.GetFieldAsString(iField)))
                        else:
                            outFeature.SetField(map['dst'], poFeature.GetFieldAsString(iField))

                        # for the icons do a lookup
                        if map['dst'] == 'sym':
                            all_icons.add(value)                            
                            if value in icon_mapping:
                                outFeature.SetField(map['dst'], str(icon_mapping[value]))
                                has_S57sym = True
                            else:
                                outFeature.SetField(map['dst'], poFeature.GetFieldAsString(iField))
                                has_S57sym =  poFeature.GetFieldAsString(iField)
                                if value not in missing:
                                    missing.append(value)

                    except UnicodeEncodeError:
                        # For Python3 on non-UTF8 strings
                        print('pynonUT', errno)
                        # exit()
                        line = line + "%s" % (poFeature.GetFieldAsBinary(iField))
                else:
                    line = line + "(null)"
                if debugging:
                    print(line)

            if has_S57sym == False:
                outFeature.SetField('sym', "NoS57Sym")
                print('No S57sym. Setting to nosymbol for:', outFeature.GetField('name'))
                description.append('No Boei icon available in source data!')

            if len(description) > 0:
                outFeature.SetField('desc', '\n'.join(description))
            outLayer.CreateFeature(outFeature)
            # dereference the feature
            outFeature = None

            poFeature = poLayer.GetNextFeature()
    reader.Destroy()
    outDataSource.Destroy()
    all_icons_allFiles[input_filename]=all_icons


def create_GPXheader(gpx):

    gpx.creator = 'boeien_generator.py -- https://github.com/marcelrv/OpenCPN-Waypoints'
    gpx.author_name = 'Marcel Verpaalen'
    gpx.copyright_year = '2022'
    gpx.copyright_license = 'CC BY-NC-SA 4.0'
    # removed to avoid everyday updates of the file without real changes
    # gpx.time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
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
    print("Saved to %s" % filename)


def update_source_data(fn, urls):
    for url in urls:  # multiple urls to be implemented
        if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > max_age:
            print('Downloading %s' % fn)
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
        print(f'GPX with {str(waypoints)} waypoints SKIPPED: {fn}')
        return
    f = open(fn, "w")
    f.write(gpx.to_xml())
    f.close()
    print(f'GPX with {str(waypoints)} points exported to {fn}')


if __name__ == "__main__":
    _UseScale = True
    _ScaleMin = 100000

    for boeien_bestand in [nederland, friesland]:
        update_source_data(boeien_bestand.source_filename, boeien_bestand.url)
        process_gml(boeien_bestand.source_filename, boeien_bestand.outputFileName, boeien_bestand.field_mapping,
                    boeien_bestand.icon_mapping, boeien_bestand.epsg)

        # post processing as it is unclear how to do in with gdal
        gpx_file = open(boeien_bestand.outputFileName, 'r')
        gpx = gpxpy.parse(gpx_file)
        create_GPXheader(gpx)
        gpx.waypoints = sorted(gpx.waypoints, key=lambda w:
                               str(w.name) + str(w.latitude + w.longitude))
        gpx.description = '%s buoys based on RWS data. Use associated user icons to display buoys shape correctly' \
            % boeien_bestand.name
        if _UseScale:
            root = create_GPX_namespace(gpx, _ScaleMin)
            for gpx_wps in gpx.waypoints:
                gpx_wps.extensions.append(root)
        saveGPX(gpx, boeien_bestand.outputFileName)

    print('All used icons:')
    for input_filename, all_icons in all_icons_allFiles.items():
        print(f'Used icons in file: {input_filename}')   
        for icon in sorted(all_icons):
            #print("'%s'," % icon)
            pass

    if len(missing) > 0:
        print('TYPE_OMSCHRIJVING missing in the mapping:')
        for m in sorted(missing):
            print("('%s' , '0')," % m)

