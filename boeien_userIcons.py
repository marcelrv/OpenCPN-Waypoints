#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create usericons for OpenCPN boeienbestand

@author: Marcel Verpaalen
"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2022"
__license__ = "AGPL 3.0"
__version__ = "1.0.0"
import json
import os
import time
import base64
import requests
from zipfile import ZipFile


workingFolder = './working/'
input_filename = workingFolder + 'iconsource.json'
outputFileName = './chartcatalog/usericons.zip'

url = 'https://geoservices.rijkswaterstaat.nl/arcgis2/rest/services/GDR/vaarweg_markeringen/MapServer/legend?f=pjson'


def saveJson(filename, data):
    safeFile(filename, json.dumps(data, indent=2))


def readJson(filename):
    with open(filename) as f:
        return json.load(f)


def safeFile(filename, indata):
    f = open(filename, "w", encoding='utf-8')
    f.write(indata)
    f.close()
    print("Exported to " + filename)


def zip_images(filename: str, file_list):
    with ZipFile(filename, 'w') as zip:
        for fn in file_list:
            zip.write(fn)
    print('Zipped to %s' % filename)


def update_source_data(fn):
    if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > 60*60*24:
        print('Downloading %s' % fn)
        response = requests.get(url)
        data = response.text
        safeFile(fn, data)
    else:
        print(
            f'Reusing existing {fn} which is {int((time.time() -  os.path.getmtime(fn))/3600)} hours old')

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

if __name__ == "__main__":
    update_source_data(input_filename)
    sourceData = readJson(input_filename)
    file_list = []
    icons = dict()
    for layer in sourceData.get('layers'):
        print('Layer: %s' % layer.get('layerName'))
        for icon in layer.get('legend'):
            ids = icon.get('values')
            if ids is None:
                ids = ['NoS57Sym']
            elif ids[0] == "<Null>":
                ids = ['NoS57Id']

            label = icon.get('label')
            print('%s: %s' % (ids[0], label))
            imageData = icon.get('imageData')
            contentType = icon.get('contentType')
            fn = '%s%s.%s' % (workingFolder, ids[0],  contentType.split('/')[1])
            

            if label in symb:
                print(label,ids[0])

            if imageData is not None and contentType is not None and fn not in file_list :
                image_64_decode = base64.b64decode(imageData)
                image_result = open(fn, 'wb')  # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                file_list.append(fn)
                icons[ids[0]] = label
    print(icons)
    zip_images(outputFileName, file_list)

