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


if __name__ == "__main__":
    update_source_data(input_filename)
    sourceData = readJson(input_filename)
    file_list = []
    icons = dict()
    mapping = dict()
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
            for id in ids:
                mapping[id] = {'id': ids[0], 'label': label}
            if imageData is not None and contentType is not None and fn not in file_list:
                image_64_decode = base64.b64decode(imageData)
                image_result = open(fn, 'wb')  # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                file_list.append(fn)
                icons[ids[0]] = label
    zip_images(outputFileName, file_list)

    print('# Mapping tabel')
    for m in mapping:
        print("('%s' , '%s'), # %s" % (m,  mapping[m].get('id'), mapping[m].get('label')))
