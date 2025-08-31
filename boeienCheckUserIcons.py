
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small helpder to check if icon is in the legend of RWS

@author: Marcel Verpaalen
"""
__author__ = "Marcel Verpaalen"
__copyright__ = "Copyright 2025"
__license__ = "AGPL 3.0"
__version__ = "1.0.0"
import json
from logging import warn
import os
import time
import requests


url = 'https://geo.rijkswaterstaat.nl/arcgis/rest/services/GDR/vaarweg_markeringen/MapServer/legend?f=pjson'



workingFolder = './UserIcons/'
input_filename = workingFolder + 'iconsource.json'
outputFileName = './chartcatalog/usericons.zip'
max_age = 60 * 60 * 24  # 24h




used_icons=['1001',
'1002',
'1003',
'1004',
'1005',
'1006',
'1007',
'1008',
'1041',
'1042',
'1043',
'1044',
'1045',
'1046',
'1047',
'1048',
'1101',
'1102',
'1103',
'1104',
'1105',
'1106',
'1107',
'1108',
'1123',
'1141',
'1142',
'1143',
'1144',
'1145',
'1146',
'1147',
'1148',
'1201',
'1202',
'1211',
'1212',
'1251',
'1252',
'1261',
'1262',
'1302',
'1312',
'1321',
'1322',
'1352',
'1362',
'1371',
'1372',
'1411',
'1412',
'1421',
'1422',
'1502',
'1511',
'1512',
'1551',
'1552',
'1561',
'1562',
'1564',
'1632',
'2012',
'2021',
'2023',
'2024',
'2031',
'2032',
'2033',
'2034',
'2123',
'2124',
'2131',
'2132',
'2133',
'2134',
'2211',
'2223',
'2231',
'2232',
'2233',
'2234',
'2314',
'2323',
'2331',
'2332',
'2333',
'2334',
'3007',
'3009',
'3031',
'3057',
'3059',
'3068',
'3071',
'3118',
'3125',
'3156',
'3175',
'3205',
'3209',
'3226',
'3229',
'3268',
'3306',
'3309',
'3327',
'3507',
'3525',
'3528',
'3530',
'3531',
'3552',
'3553',
'3557',
'3559',
'3566',
'3568',
'3571',
'3573',
'3577',
'3580',
'3581',
'3583',
'3631',
'3653',
'3656',
'3657',
'3726',
'3729',
'3756',
'3775',
'3782',
'3803',
'3806',
'3811',
'3827',
'3856',
'3868',
'4026',
'4030',
'4068',
'4080',
'4106',
'4156',
'4206',
'4233',
'4253',
'4256',
'4257',
'4306',
'4318',
'4333',
'4335',
'4382',
'5002',
'5003',
'5006',
'5007',
'5009',
'5011',
'5018',
'5023',
'5025',
'5026',
'5027',
'5031',
'5054',
'5056',
'5057',
'5059',
'5061',
'5065',
'5066',
'5068',
'5069',
'5077',
'5079',
'5080',
'5082',
'5103',
'5104',
'5105',
'5106',
'5107',
'5109',
'5111',
'5112',
'5118',
'5123',
'5125',
'5126',
'5127',
'5130',
'5131',
'5132',
'5135',
'5149',
'5153',
'5159',
'5168',
'5173',
'5175',
'5176',
'5177',
'5179',
'5185',
'5306',
'5309',
'5318',
'5326',
'5327',
'5332',
'5334',
'5356',
'5377',
'5441',
'5501',
'5502',
'5511',
'5512',
'5521',
'554',
'5541',
'5542',
'5547',
'6001',
'6005',
'6006',
'6007',
'6023',
'6033',
'6034',
'6041',
'6042']


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

def update_source_data(fn,url):
    if not os.path.exists(fn) or (time.time() - os.path.getmtime(fn)) > max_age:
        print('Downloading %s' % fn)
        response = requests.get(url)
        data = response.text
        safeFile(fn, data)
    else:
        print(
            f'Reusing existing {fn} which is {int((time.time() -  os.path.getmtime(fn))/3600)} hours old')
        

if __name__ == "__main__":
    os.makedirs(workingFolder, exist_ok=True)
    update_source_data(input_filename,url)
    sourceData = readJson(input_filename)
    file_list = []
    icons = dict()
    mapping = dict()
    no_sym = 0
    missingIcons = set()
    for layer in sourceData.get('layers'):
        print('Layer: %s' % layer.get('layerName'))
        for icon in layer.get('legend'):
            ids = icon.get('values')
            # handle some specials
            if ids is None:
                ids = ['NoS57Sym' + '-' + str(no_sym)]
                no_sym += 1
            elif ids[0] == "<Null>":
                ids = ['NoS57Id']
            if not ids[0].isnumeric():
                if len(ids) > 1:
                    ids[0] = '-'.join(ids[0:2])
                print('Special:', ids[0], icon.get('label'), ids)
            ids[0] = ids[0].replace('/', '-').replace(' ', '_')
            label = icon.get('label')
            # print('%s: %s' % (ids[0], label))
            imageData = icon.get('imageData')
            contentType = icon.get('contentType')
            fn = '%s%s.%s' % (workingFolder, ids[0], contentType.split('/')[1])
            for id in ids:
                mapping[id] = {'id': ids[0], 'label': label}
    for id in used_icons:
        if id in mapping:
            pass
        else:
            print('S57 id %s not found!' % id)
            missingIcons.add(id)
    
    boeienURL = "https://geo.rijkswaterstaat.nl/services/ogc/gdr/vaarweg_markeringen/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=vaarweg_markering_drijvend_detail&outputFormat=json"
    update_source_data(workingFolder+'boeien.json',boeienURL)
    sourceData = readJson(workingFolder+'boeien.json')
    for feature in sourceData.get('features'):
        props = feature.get('properties')
        warn=   False

        #print(props.get('vaarwater'), props.get('s57_id'))
        if 's57_id' in props:
            if props.get('s57_id') is None:
                print('No S57Id for:', feature.get('id'), props.get('vaarwater'), props.get('benaming'))
                warn =True
            id = str(props.get('s57_id'))
            if  id in missingIcons or id is None:
                 warn =True
            if id is "":
                print('No S57Id for:', feature.get('id'), props.get('vaarwater'), props.get('benaming'))
#                id = 'NoS57Id'
                warn =True

        else:
            warn = True
            print('No S57sym for:', feature.get('id'), props.get('vaarwater'), props.get('benaming'))
        #         break
        if warn:
            print(feature.get('id'), props.get('vaarwater'), props.get('benaming'), "S57sym: " ,props.get('s57_id'))
        
