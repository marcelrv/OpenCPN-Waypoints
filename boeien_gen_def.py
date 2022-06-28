#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source definitions 
note: requires python > 3.9 otherwise 'TypeError: 'type' object is not subscriptable' errors
@author: Marcel Verpaalen

"""

workingFolder = './working/'


class BoeienSource:

    def __init__(self, name: str, source_filename: str, outputFileName: str, url: list[str],
                 field_mapping: dict[str, str], icon_mapping: dict[str, str], epsg=None):
        self.name: str = name
        self.source_filename: str = source_filename
        self.outputFileName: str = outputFileName
        self.url: list[str] = url
        self.field_mapping: dict[str, str] = field_mapping
        self.icon_mapping: dict[str, str] = icon_mapping
        self.epsg = epsg


nederland = BoeienSource(
    name='Nederland',
    source_filename=workingFolder + 'NL-Boeien.gml',
    outputFileName='NL-Boeien.gpx',
    url=['https://geo.rijkswaterstaat.nl/services/ogc/gdr/vaarweg_markeringen/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=vaarweg_markering_drijvend_detail&outputFormat=gml32'],

    # mapping Vaarwegmarkeringen feature naam naar GPX field
    field_mapping=dict([('BENAMING', {'dst': 'name', 'isDescription': False}),
                        ('S57_ID', {'dst': 'sym', 'isDescription': False}),
                        ('VAARWATER', {'dst': 'vaarweg', 'isDescription': True}),
                        ('SIGN_KAR', {'dst': 'licht type', 'isDescription': True}),
                        ('SIGN_PERIO', {'dst': 'licht periode', 'isDescription': True}),
                        ('VORM_KLEUR', {'dst': 'model', 'isDescription': True}),
                        ('LICHT_KLR', {'dst': 'lich kleur', 'isDescription': True})
                        ]),
    # Mapping van boei  S57 type naar icon
    icon_mapping=dict([
        ('NoS57Sym', 'NoS57Sym'),
        ('1001', '1001'),  # Groen spits
        ('1002', '1001'),  # Groen spits
        ('1003', '1003'),  # Groen spits met kegelpunt omhoog
        ('1004', '1003'),  # Groen spits met kegelpunt omhoog
        ('1005', '1005'),  # Groen spits met groen licht
        ('1006', '1005'),  # Groen spits met groen licht
        ('1008', '1008'),  # Groen spits met kegelpunt omhoog en groen licht
        ('1007', '1008'),  # Groen spits met kegelpunt omhoog en groen licht
        ('1021', '1021'),  # Groen pilaar
        ('1022', '1021'),  # Groen pilaar
        ('1023', '1023'),  # Groen pilaar met kegelpunt omhoog
        ('1024', '1023'),  # Groen pilaar met kegelpunt omhoog
        ('1025', '1025'),  # Groen pilaar en groen licht
        ('1026', '1025'),  # Groen pilaar en groen licht
        ('1027', '1027'),  # Groen pilaar met kegelpunt omhoog en groen licht
        ('1028', '1027'),  # Groen pilaar met kegelpunt omhoog en groen licht
        ('1041', '1041'),  # Groen spar
        ('1042', '1041'),  # Groen spar
        ('1043', '1043'),  # Groen spar met kegelpunt omhoog
        ('1044', '1043'),  # Groen spar met kegelpunt omhoog
        ('1045', '1045'),  # Groen spar met groen licht
        ('1046', '1045'),  # Groen spar met groen licht
        ('1047', '1047'),  # Groen spar met kegelpunt omhoog en groen licht
        ('1048', '1047'),  # Groen spar met kegelpunt omhoog en groen licht
        ('1101', '1101'),  # Rood stomp
        ('1102', '1101'),  # Rood stomp
        ('1103', '1103'),  # Rood stomp met rode cilinder
        ('1104', '1103'),  # Rood stomp met rode cilinder
        ('1105', '1105'),  # Rood stomp met rood licht
        ('1106', '1105'),  # Rood stomp met rood licht
        ('1107', '1107'),  # Rood stomp met rode cilinder en rood licht
        ('1108', '1107'),  # Rood stomp met rode cilinder en rood licht
        ('1121', '1121'),  # Rood pilaar
        ('1122', '1121'),  # Rood pilaar
        ('1123', '1123'),  # Rood pilaar met rode cilinder
        ('1124', '1123'),  # Rood pilaar met rode cilinder
        ('1125', '1125'),  # Rood pilaar met rood licht
        ('1126', '1125'),  # Rood pilaar met rood licht
        ('1127', '1127'),  # Rood pilaar met rode cilinder en rood licht
        ('1128', '1127'),  # Rood pilaar met rode cilinder en rood licht
        ('1141', '1141'),  # Rood spar
        ('1142', '1141'),  # Rood spar
        ('1143', '1143'),  # Rood spar met rode cilinder
        ('1144', '1143'),  # Rood spar met rode cilinder
        ('1145', '1145'),  # Rood spar met rood licht
        ('1146', '1145'),  # Rood spar met rood licht
        ('1147', '1147'),  # Rood spar met rode cilinder en rood licht
        ('1148', '1147'),  # Rood spar met rode cilinder en rood licht
        ('1201', '1201'),  # Groen rood bol met kegelpunt omhoog
        ('1202', '1202'),  # Groen rood bol met kegelpunt omhoog en groen licht
        ('1211', '1211'),  # Groen rood spar met groene bol en kegelpunt omhoog
        ('1212', '1212'),  # Groen rood spar met groene bol en kegelpunt omhoog en groen licht
        ('1251', '1251'),  # Rood groen bol met cilinder
        ('1252', '1252'),  # Rood groen bol met cilinder en rood licht
        ('1261', '1261'),  # Rood groen spar met rode bol en cilinder
        ('1262', '1262'),  # Rood groen spar met rode bol en cilinder en rood licht
        ('1301', '1301'),  # Groen rood groen spits
        ('1302', '1302'),  # Groen rood groen spits met groen licht
        ('1311', '1311'),  # Groen rood groen pilaar met kegelpunt omhoog
        ('1312', '1312'),  # Groen rood groen pilaar met kegelpunt omhoog en groen licht
        ('1321', '1321'),  # Groen rood groen spar met groene kegelpunt omhoog
        ('1322', '1322'),  # Groen rood groen spar met groene kegel omhoog en groen licht
        ('1351', '1351'),  # Rood groen rood stomp
        ('1352', '1352'),  # Rood groen rood stomp met rood licht
        ('1361', '1361'),  # Rood groen rood pilaar met cilinder
        ('1362', '1362'),  # Rood groen rood pilaar met cilinder en rood licht
        ('1371', '1371'),  # Rood groen rood spar met rode cilinder
        ('1372', '1372'),  # Rood groen rood spar met rode cilinder en rood licht
        ('1401', '1401'),  # Rood groen rood groen rood pilaar met rode bol
        ('1402', '1402'),  # Rood groen rood groen rood pilaar met rode bol en rood licht
        ('1411', '1411'),  # Rood groen rood groen rood bol met rode bol
        ('1412', '1412'),  # Rood groen rood groen rood bol met rode bol en rood licht
        ('1421', '1421'),  # Rood groen rood groen rood spar met rood groene bol
        ('1422', '1422'),  # Rood groen rood groen rood spar met rood groene bol en wit licht
        ('1501', '1501'),  # Groen wit groen wit groen spits
        ('1502', '1502'),  # Groen wit groen wit groen spits met kegelpunt omhoog
        ('1503', '1503'),  # Groen wit groen wit groen spits met groen licht
        ('1504', '1504'),  # Groen wit groen wit groen spits met kegelpunt omhoog en groen licht
        ('1511', '1511'),  # Groen wit groen wit groen spar
        ('1512', '1512'),  # Groen wit groen wit groen spar met kegelpunt omhoog
        ('1513', '1513'),  # Groen wit groen wit groen spar met groen licht
        ('1514', '1514'),  # Groen wit groen wit groen spar met kegelpunt omhoog en groen licht
        ('1551', '1551'),  # Rood wit rood wit rood stomp
        ('1552', '1552'),  # Rood wit rood wit rood stomp met cilinder
        ('1553', '1553'),  # Rood wit rood wit rood stomp met rood licht
        ('1554', '1554'),  # Rood wit rood wit rood stomp met cilinder en rood licht
        ('1561', '1561'),  # Rood wit rood wit rood spar
        ('1562', '1562'),  # Rood wit rood wit rood spar met cilinder
        ('1563', '1563'),  # Rood wit rood wit rood spar met rood licht
        ('1564', '1564'),  # Rood wit rood wit rood spar met cilinder en rood licht
        ('1601', '1601'),  # Groen wit groen wit groen spits
        ('1602', '1602'),  # Groen wit groen wit groen spits met kegelpunt omhoog
        ('1603', '1603'),  # Groen wit groen wit groen spits met groen licht
        ('1604', '1604'),  # Groen wit groen wit groen spits met kegelpunt omhoog en groen licht
        ('1611', '1611'),  # Groen wit groen wit groen spar
        ('1612', '1612'),  # Groen wit groen wit groen spar met kegelpunt omhoog
        ('1613', '1613'),  # Groen wit groen wit groen spar met groen licht
        ('1614', '1614'),  # Groen wit groen wit groen spar met kegelpunt omhoog en groen licht
        ('1621', '1621'),  # Rood wit rood wit rood stomp
        ('1622', '1622'),  # Rood wit rood wit rood stomp met cilinder
        ('1623', '1623'),  # Rood wit rood wit rood stomp met rood licht
        ('1624', '1624'),  # Rood wit rood wit rood stomp met cilinder en rood licht
        ('1631', '1631'),  # Rood wit rood wit rood spar
        ('1632', '1632'),  # Rood wit rood wit rood spar met cilinder
        ('1633', '1633'),  # Rood wit rood wit rood spar met rood licht
        ('1634', '1634'),  # Rood wit rood wit rood spar met cilinder en rood licht
        ('2001', '2001'),  # Zwart geel spits met 2 kegels punten omhoog
        ('2002', '2001'),  # Zwart geel spits met 2 kegels punten omhoog
        ('2003', '2003'),  # Zwart geel spits met 2 kegels punten omhoog en wit licht
        ('2004', '2003'),  # Zwart geel spits met 2 kegels punten omhoog en wit licht
        ('2011', '2011'),  # Zwart geel stomp met 2 kegels punten omhoog
        ('2012', '2011'),  # Zwart geel stomp met 2 kegels punten omhoog
        ('2013', '2013'),  # Zwart geel stomp met 2 kegels punten omhoog en wit licht
        ('2014', '2013'),  # Zwart geel stomp met 2 kegels punten omhoog en wit licht
        ('2021', '2021'),  # Zwart geel pilaar met 2 kegels punten omhoog
        ('2022', '2021'),  # Zwart geel pilaar met 2 kegels punten omhoog
        ('2023', '2023'),  # Zwart geel pilaar met 2 kegels punten omhoog en wit licht
        ('2024', '2023'),  # Zwart geel pilaar met 2 kegels punten omhoog en wit licht
        ('2031', '2031'),  # Zwart geel spar met 2 kegels punten omhoog
        ('2032', '2031'),  # Zwart geel spar met 2 kegels punten omhoog
        ('2033', '2033'),  # Zwart geel spar met 2 kegels punten omhoog en wit licht
        ('2034', '2033'),  # Zwart geel spar met 2 kegels punten omhoog en wit licht
        ('2101', '2101'),  # Zwart geel zwart spits met 2 kegels basis naar elkaar toe
        ('2102', '2101'),  # Zwart geel zwart spits met 2 kegels basis naar elkaar toe
        ('2103', '2103'),  # Zwart geel zwart spits met 2 kegels basis naar elkaar toe en wit licht
        ('2104', '2103'),  # Zwart geel zwart spits met 2 kegels basis naar elkaar toe en wit licht
        ('2111', '2111'),  # Zwart geel zwart stomp 2 kegel basis naar elkaar
        ('2112', '2111'),  # Zwart geel zwart stomp 2 kegel basis naar elkaar
        ('2113', '2113'),  # Zwart geel zwart stomp 2 kegel basis naar elkaar met wit licht
        ('2114', '2113'),  # Zwart geel zwart stomp 2 kegel basis naar elkaar met wit licht
        ('2121', '2121'),  # Zwart geel zwart pilaar met 2 kegels basis naar elkaar
        ('2122', '2121'),  # Zwart geel zwart pilaar met 2 kegels basis naar elkaar
        ('2123', '2123'),  # Zwart geel zwart pilaar met 2 kegels basis naar elkaar met wit licht
        ('2124', '2123'),  # Zwart geel zwart pilaar met 2 kegels basis naar elkaar met wit licht
        ('2131', '2131'),  # Zwart geel zwart spar met 2 kegels basis naar elkaar
        ('2132', '2131'),  # Zwart geel zwart spar met 2 kegels basis naar elkaar
        ('2133', '2133'),  # Zwart geel zwart spar met 2 kegels basis naar elkaar met wit licht
        ('2134', '2133'),  # Zwart geel zwart spar met 2 kegels basis naar elkaar met wit licht
        ('2201', '2201'),  # Geel zwart spits met 2 kegels omlaag
        ('2202', '2201'),  # Geel zwart spits met 2 kegels omlaag
        ('2203', '2203'),  # Geel zwart spits met 2 kegels omlaag en wit licht
        ('2204', '2203'),  # Geel zwart spits met 2 kegels omlaag en wit licht
        ('2211', '2211'),  # Geel zwart stomp met 2 kegels punten omlaag
        ('2212', '2211'),  # Geel zwart stomp met 2 kegels punten omlaag
        ('2213', '2213'),  # Geel zwart stomp met 2 kegels punten omlaag met wit licht
        ('2214', '2213'),  # Geel zwart stomp met 2 kegels punten omlaag met wit licht
        ('2221', '2221'),  # Geel zwart pilaar met 2 kegels punten omlaag
        ('2222', '2221'),  # Geel zwart pilaar met 2 kegels punten omlaag
        ('2223', '2223'),  # Geel zwart pilaar met 2 kegels omlaag en wit licht
        ('2224', '2223'),  # Geel zwart pilaar met 2 kegels omlaag en wit licht
        ('2231', '2231'),  # Geel zwart spar met 2 kegels punten omlaag
        ('2232', '2231'),  # Geel zwart spar met 2 kegels punten omlaag
        ('2233', '2233'),  # Geel zwart spar met 2 kegels punten omlaag en wit licht
        ('2234', '2233'),  # Geel zwart spar met 2 kegels punten omlaag en wit licht
        ('2301', '2301'),  # Geel zwart geel spits met 2 kegels punten naar elkaar
        ('2302', '2301'),  # Geel zwart geel spits met 2 kegels punten naar elkaar
        ('2303', '2303'),  # Geel zwart geel spits met 2 kegels punten naar elkaar en wit licht
        ('2304', '2303'),  # Geel zwart geel spits met 2 kegels punten naar elkaar en wit licht
        ('2311', '2311'),  # Geel zwart geel stomp met 2 kegels punten naar elkaar
        ('2312', '2311'),  # Geel zwart geel stomp met 2 kegels punten naar elkaar
        ('2313', '2313'),  # Geel zwart geel stomp met 2 kegels punten naar elkaar en wit licht
        ('2314', '2313'),  # Geel zwart geel stomp met 2 kegels punten naar elkaar en wit licht
        ('2321', '2321'),  # Geel zwart geel pilaar met 2 kegels punten naar elkaar
        ('2322', '2321'),  # Geel zwart geel pilaar met 2 kegels punten naar elkaar
        ('2323', '2323'),  # Geel zwart geel pilaar met 2 kegels punten naar elkaar en wit licht
        ('2324', '2323'),  # Geel zwart geel pilaar met 2 kegels punten naar elkaar en wit licht
        ('2331', '2331'),  # Geel zwart geel spar met 2 kegels punten naar elkaar
        ('2332', '2331'),  # Geel zwart geel spar met 2 kegels punten naar elkaar
        ('2333', '2333'),  # Geel zwart geel spar met 2 kegels punten naar elkaar en wit licht
        ('2334', '2333'),  # Geel zwart geel spar met 2 kegels punten naar elkaar en wit licht
        ('3001', '3001'),  # Geel spits
        ('3002', '3001'),  # Geel spits
        ('3003', '3001'),  # Geel spits
        ('3004', '3001'),  # Geel spits
        ('3005', '3001'),  # Geel spits
        ('3006', '3001'),  # Geel spits
        ('3007', '3001'),  # Geel spits
        ('3008', '3001'),  # Geel spits
        ('3009', '3001'),  # Geel spits
        ('3010', '3001'),  # Geel spits
        ('3011', '3001'),  # Geel spits
        ('3012', '3001'),  # Geel spits
        ('3013', '3001'),  # Geel spits
        ('3014', '3001'),  # Geel spits
        ('3015', '3001'),  # Geel spits
        ('3016', '3001'),  # Geel spits
        ('3017', '3001'),  # Geel spits
        ('3018', '3001'),  # Geel spits
        ('3019', '3001'),  # Geel spits
        ('3020', '3001'),  # Geel spits
        ('3021', '3001'),  # Geel spits
        ('3022', '3001'),  # Geel spits
        ('3023', '3001'),  # Geel spits
        ('3024', '3001'),  # Geel spits
        ('3025', '3001'),  # Geel spits
        ('3026', '3001'),  # Geel spits
        ('3027', '3001'),  # Geel spits
        ('3028', '3001'),  # Geel spits
        ('3029', '3001'),  # Geel spits
        ('3030', '3001'),  # Geel spits
        ('3031', '3001'),  # Geel spits
        ('3032', '3001'),  # Geel spits
        ('3033', '3001'),  # Geel spits
        ('3034', '3001'),  # Geel spits
        ('3035', '3001'),  # Geel spits
        ('3050', '3001'),  # Geel spits
        ('3051', '3001'),  # Geel spits
        ('3052', '3001'),  # Geel spits
        ('3053', '3001'),  # Geel spits
        ('3054', '3001'),  # Geel spits
        ('3055', '3001'),  # Geel spits
        ('3056', '3001'),  # Geel spits
        ('3057', '3001'),  # Geel spits
        ('3058', '3001'),  # Geel spits
        ('3059', '3001'),  # Geel spits
        ('3060', '3001'),  # Geel spits
        ('3061', '3001'),  # Geel spits
        ('3062', '3001'),  # Geel spits
        ('3063', '3001'),  # Geel spits
        ('3064', '3001'),  # Geel spits
        ('3065', '3001'),  # Geel spits
        ('3066', '3001'),  # Geel spits
        ('3067', '3001'),  # Geel spits
        ('3068', '3001'),  # Geel spits
        ('3069', '3001'),  # Geel spits
        ('3070', '3001'),  # Geel spits
        ('3071', '3001'),  # Geel spits
        ('3072', '3001'),  # Geel spits
        ('3073', '3001'),  # Geel spits
        ('3074', '3001'),  # Geel spits
        ('3075', '3001'),  # Geel spits
        ('3076', '3001'),  # Geel spits
        ('3077', '3001'),  # Geel spits
        ('3078', '3001'),  # Geel spits
        ('3079', '3001'),  # Geel spits
        ('3080', '3001'),  # Geel spits
        ('3081', '3001'),  # Geel spits
        ('3082', '3001'),  # Geel spits
        ('3083', '3001'),  # Geel spits
        ('3084', '3001'),  # Geel spits
        ('3085', '3001'),  # Geel spits
        ('3101', '3101'),  # Geel spits met liggend kruis
        ('3102', '3101'),  # Geel spits met liggend kruis
        ('3103', '3101'),  # Geel spits met liggend kruis
        ('3104', '3101'),  # Geel spits met liggend kruis
        ('3105', '3101'),  # Geel spits met liggend kruis
        ('3106', '3101'),  # Geel spits met liggend kruis
        ('3107', '3101'),  # Geel spits met liggend kruis
        ('3108', '3101'),  # Geel spits met liggend kruis
        ('3109', '3101'),  # Geel spits met liggend kruis
        ('3110', '3101'),  # Geel spits met liggend kruis
        ('3111', '3101'),  # Geel spits met liggend kruis
        ('3112', '3101'),  # Geel spits met liggend kruis
        ('3113', '3101'),  # Geel spits met liggend kruis
        ('3114', '3101'),  # Geel spits met liggend kruis
        ('3115', '3101'),  # Geel spits met liggend kruis
        ('3116', '3101'),  # Geel spits met liggend kruis
        ('3117', '3101'),  # Geel spits met liggend kruis
        ('3118', '3101'),  # Geel spits met liggend kruis
        ('3119', '3101'),  # Geel spits met liggend kruis
        ('3120', '3101'),  # Geel spits met liggend kruis
        ('3121', '3101'),  # Geel spits met liggend kruis
        ('3122', '3101'),  # Geel spits met liggend kruis
        ('3123', '3101'),  # Geel spits met liggend kruis
        ('3124', '3101'),  # Geel spits met liggend kruis
        ('3125', '3101'),  # Geel spits met liggend kruis
        ('3126', '3101'),  # Geel spits met liggend kruis
        ('3127', '3101'),  # Geel spits met liggend kruis
        ('3128', '3101'),  # Geel spits met liggend kruis
        ('3129', '3101'),  # Geel spits met liggend kruis
        ('3130', '3101'),  # Geel spits met liggend kruis
        ('3131', '3101'),  # Geel spits met liggend kruis
        ('3132', '3101'),  # Geel spits met liggend kruis
        ('3133', '3101'),  # Geel spits met liggend kruis
        ('3134', '3101'),  # Geel spits met liggend kruis
        ('3135', '3101'),  # Geel spits met liggend kruis
        ('3151', '3101'),  # Geel spits met liggend kruis
        ('3152', '3101'),  # Geel spits met liggend kruis
        ('3153', '3101'),  # Geel spits met liggend kruis
        ('3154', '3101'),  # Geel spits met liggend kruis
        ('3155', '3101'),  # Geel spits met liggend kruis
        ('3156', '3101'),  # Geel spits met liggend kruis
        ('3157', '3101'),  # Geel spits met liggend kruis
        ('3158', '3101'),  # Geel spits met liggend kruis
        ('3159', '3101'),  # Geel spits met liggend kruis
        ('3160', '3101'),  # Geel spits met liggend kruis
        ('3161', '3101'),  # Geel spits met liggend kruis
        ('3162', '3101'),  # Geel spits met liggend kruis
        ('3163', '3101'),  # Geel spits met liggend kruis
        ('3164', '3101'),  # Geel spits met liggend kruis
        ('3165', '3101'),  # Geel spits met liggend kruis
        ('3166', '3101'),  # Geel spits met liggend kruis
        ('3167', '3101'),  # Geel spits met liggend kruis
        ('3168', '3101'),  # Geel spits met liggend kruis
        ('3169', '3101'),  # Geel spits met liggend kruis
        ('3170', '3101'),  # Geel spits met liggend kruis
        ('3171', '3101'),  # Geel spits met liggend kruis
        ('3172', '3101'),  # Geel spits met liggend kruis
        ('3173', '3101'),  # Geel spits met liggend kruis
        ('3174', '3101'),  # Geel spits met liggend kruis
        ('3175', '3101'),  # Geel spits met liggend kruis
        ('3176', '3101'),  # Geel spits met liggend kruis
        ('3177', '3101'),  # Geel spits met liggend kruis
        ('3178', '3101'),  # Geel spits met liggend kruis
        ('3179', '3101'),  # Geel spits met liggend kruis
        ('3180', '3101'),  # Geel spits met liggend kruis
        ('3181', '3101'),  # Geel spits met liggend kruis
        ('3182', '3101'),  # Geel spits met liggend kruis
        ('3183', '3101'),  # Geel spits met liggend kruis
        ('3184', '3101'),  # Geel spits met liggend kruis
        ('3185', '3101'),  # Geel spits met liggend kruis
        ('3201', '3201'),  # Geel spits met geel licht
        ('3202', '3201'),  # Geel spits met geel licht
        ('3203', '3201'),  # Geel spits met geel licht
        ('3204', '3201'),  # Geel spits met geel licht
        ('3205', '3201'),  # Geel spits met geel licht
        ('3206', '3201'),  # Geel spits met geel licht
        ('3207', '3201'),  # Geel spits met geel licht
        ('3208', '3201'),  # Geel spits met geel licht
        ('3209', '3201'),  # Geel spits met geel licht
        ('3210', '3201'),  # Geel spits met geel licht
        ('3211', '3201'),  # Geel spits met geel licht
        ('3212', '3201'),  # Geel spits met geel licht
        ('3213', '3201'),  # Geel spits met geel licht
        ('3214', '3201'),  # Geel spits met geel licht
        ('3215', '3201'),  # Geel spits met geel licht
        ('3216', '3201'),  # Geel spits met geel licht
        ('3217', '3201'),  # Geel spits met geel licht
        ('3218', '3201'),  # Geel spits met geel licht
        ('3219', '3201'),  # Geel spits met geel licht
        ('3220', '3201'),  # Geel spits met geel licht
        ('3221', '3201'),  # Geel spits met geel licht
        ('3222', '3201'),  # Geel spits met geel licht
        ('3223', '3201'),  # Geel spits met geel licht
        ('3224', '3201'),  # Geel spits met geel licht
        ('3225', '3201'),  # Geel spits met geel licht
        ('3226', '3201'),  # Geel spits met geel licht
        ('3227', '3201'),  # Geel spits met geel licht
        ('3228', '3201'),  # Geel spits met geel licht
        ('3229', '3201'),  # Geel spits met geel licht
        ('3230', '3201'),  # Geel spits met geel licht
        ('3231', '3201'),  # Geel spits met geel licht
        ('3232', '3201'),  # Geel spits met geel licht
        ('3233', '3201'),  # Geel spits met geel licht
        ('3234', '3201'),  # Geel spits met geel licht
        ('3235', '3201'),  # Geel spits met geel licht
        ('3251', '3201'),  # Geel spits met geel licht
        ('3252', '3201'),  # Geel spits met geel licht
        ('3253', '3201'),  # Geel spits met geel licht
        ('3254', '3201'),  # Geel spits met geel licht
        ('3255', '3201'),  # Geel spits met geel licht
        ('3256', '3201'),  # Geel spits met geel licht
        ('3257', '3201'),  # Geel spits met geel licht
        ('3258', '3201'),  # Geel spits met geel licht
        ('3259', '3201'),  # Geel spits met geel licht
        ('3260', '3201'),  # Geel spits met geel licht
        ('3261', '3201'),  # Geel spits met geel licht
        ('3262', '3201'),  # Geel spits met geel licht
        ('3263', '3201'),  # Geel spits met geel licht
        ('3264', '3201'),  # Geel spits met geel licht
        ('3265', '3201'),  # Geel spits met geel licht
        ('3266', '3201'),  # Geel spits met geel licht
        ('3267', '3201'),  # Geel spits met geel licht
        ('3268', '3201'),  # Geel spits met geel licht
        ('3269', '3201'),  # Geel spits met geel licht
        ('3270', '3201'),  # Geel spits met geel licht
        ('3271', '3201'),  # Geel spits met geel licht
        ('3272', '3201'),  # Geel spits met geel licht
        ('3273', '3201'),  # Geel spits met geel licht
        ('3274', '3201'),  # Geel spits met geel licht
        ('3275', '3201'),  # Geel spits met geel licht
        ('3276', '3201'),  # Geel spits met geel licht
        ('3277', '3201'),  # Geel spits met geel licht
        ('3278', '3201'),  # Geel spits met geel licht
        ('3279', '3201'),  # Geel spits met geel licht
        ('3280', '3201'),  # Geel spits met geel licht
        ('3281', '3201'),  # Geel spits met geel licht
        ('3282', '3201'),  # Geel spits met geel licht
        ('3283', '3201'),  # Geel spits met geel licht
        ('3284', '3201'),  # Geel spits met geel licht
        ('3285', '3201'),  # Geel spits met geel licht
        ('3301', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3302', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3303', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3304', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3305', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3306', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3307', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3308', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3309', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3310', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3311', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3312', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3313', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3314', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3315', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3316', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3317', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3318', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3319', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3320', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3321', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3322', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3323', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3324', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3325', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3326', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3327', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3328', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3329', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3330', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3331', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3332', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3333', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3334', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3335', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3351', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3352', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3353', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3354', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3355', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3356', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3357', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3358', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3359', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3360', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3361', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3362', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3363', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3364', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3365', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3366', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3367', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3368', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3369', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3370', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3371', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3372', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3373', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3374', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3375', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3376', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3377', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3378', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3379', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3380', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3381', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3382', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3383', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3384', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3385', '3301'),  # Geel spits met liggend kruis en geel licht
        ('3500', '3500'),  # Geel stomp
        ('3501', '3500'),  # Geel stomp
        ('3502', '3500'),  # Geel stomp
        ('3503', '3500'),  # Geel stomp
        ('3504', '3500'),  # Geel stomp
        ('3505', '3500'),  # Geel stomp
        ('3506', '3500'),  # Geel stomp
        ('3507', '3500'),  # Geel stomp
        ('3508', '3500'),  # Geel stomp
        ('3509', '3500'),  # Geel stomp
        ('3510', '3500'),  # Geel stomp
        ('3511', '3500'),  # Geel stomp
        ('3512', '3500'),  # Geel stomp
        ('3513', '3500'),  # Geel stomp
        ('3514', '3500'),  # Geel stomp
        ('3515', '3500'),  # Geel stomp
        ('3516', '3500'),  # Geel stomp
        ('3517', '3500'),  # Geel stomp
        ('3518', '3500'),  # Geel stomp
        ('3519', '3500'),  # Geel stomp
        ('3520', '3500'),  # Geel stomp
        ('3521', '3500'),  # Geel stomp
        ('3522', '3500'),  # Geel stomp
        ('3523', '3500'),  # Geel stomp
        ('3524', '3500'),  # Geel stomp
        ('3525', '3500'),  # Geel stomp
        ('3526', '3500'),  # Geel stomp
        ('3527', '3500'),  # Geel stomp
        ('3528', '3500'),  # Geel stomp
        ('3529', '3500'),  # Geel stomp
        ('3530', '3500'),  # Geel stomp
        ('3531', '3500'),  # Geel stomp
        ('3532', '3500'),  # Geel stomp
        ('3533', '3500'),  # Geel stomp
        ('3534', '3500'),  # Geel stomp
        ('3535', '3500'),  # Geel stomp
        ('3550', '3500'),  # Geel stomp
        ('3551', '3500'),  # Geel stomp
        ('3552', '3500'),  # Geel stomp
        ('3553', '3500'),  # Geel stomp
        ('3554', '3500'),  # Geel stomp
        ('3555', '3500'),  # Geel stomp
        ('3556', '3500'),  # Geel stomp
        ('3557', '3500'),  # Geel stomp
        ('3558', '3500'),  # Geel stomp
        ('3559', '3500'),  # Geel stomp
        ('3560', '3500'),  # Geel stomp
        ('3561', '3500'),  # Geel stomp
        ('3562', '3500'),  # Geel stomp
        ('3563', '3500'),  # Geel stomp
        ('3564', '3500'),  # Geel stomp
        ('3565', '3500'),  # Geel stomp
        ('3566', '3500'),  # Geel stomp
        ('3567', '3500'),  # Geel stomp
        ('3568', '3500'),  # Geel stomp
        ('3569', '3500'),  # Geel stomp
        ('3570', '3500'),  # Geel stomp
        ('3571', '3500'),  # Geel stomp
        ('3572', '3500'),  # Geel stomp
        ('3573', '3500'),  # Geel stomp
        ('3574', '3500'),  # Geel stomp
        ('3575', '3500'),  # Geel stomp
        ('3576', '3500'),  # Geel stomp
        ('3577', '3500'),  # Geel stomp
        ('3578', '3500'),  # Geel stomp
        ('3579', '3500'),  # Geel stomp
        ('3580', '3500'),  # Geel stomp
        ('3581', '3500'),  # Geel stomp
        ('3582', '3500'),  # Geel stomp
        ('3583', '3500'),  # Geel stomp
        ('3584', '3500'),  # Geel stomp
        ('3585', '3500'),  # Geel stomp
        ('3601', '3601'),  # Geel stomp met liggend kruis
        ('3602', '3601'),  # Geel stomp met liggend kruis
        ('3603', '3601'),  # Geel stomp met liggend kruis
        ('3604', '3601'),  # Geel stomp met liggend kruis
        ('3605', '3601'),  # Geel stomp met liggend kruis
        ('3606', '3601'),  # Geel stomp met liggend kruis
        ('3607', '3601'),  # Geel stomp met liggend kruis
        ('3608', '3601'),  # Geel stomp met liggend kruis
        ('3609', '3601'),  # Geel stomp met liggend kruis
        ('3610', '3601'),  # Geel stomp met liggend kruis
        ('3611', '3601'),  # Geel stomp met liggend kruis
        ('3612', '3601'),  # Geel stomp met liggend kruis
        ('3613', '3601'),  # Geel stomp met liggend kruis
        ('3614', '3601'),  # Geel stomp met liggend kruis
        ('3615', '3601'),  # Geel stomp met liggend kruis
        ('3616', '3601'),  # Geel stomp met liggend kruis
        ('3617', '3601'),  # Geel stomp met liggend kruis
        ('3618', '3601'),  # Geel stomp met liggend kruis
        ('3619', '3601'),  # Geel stomp met liggend kruis
        ('3620', '3601'),  # Geel stomp met liggend kruis
        ('3621', '3601'),  # Geel stomp met liggend kruis
        ('3622', '3601'),  # Geel stomp met liggend kruis
        ('3623', '3601'),  # Geel stomp met liggend kruis
        ('3624', '3601'),  # Geel stomp met liggend kruis
        ('3625', '3601'),  # Geel stomp met liggend kruis
        ('3626', '3601'),  # Geel stomp met liggend kruis
        ('3627', '3601'),  # Geel stomp met liggend kruis
        ('3628', '3601'),  # Geel stomp met liggend kruis
        ('3629', '3601'),  # Geel stomp met liggend kruis
        ('3630', '3601'),  # Geel stomp met liggend kruis
        ('3631', '3601'),  # Geel stomp met liggend kruis
        ('3632', '3601'),  # Geel stomp met liggend kruis
        ('3633', '3601'),  # Geel stomp met liggend kruis
        ('3634', '3601'),  # Geel stomp met liggend kruis
        ('3635', '3601'),  # Geel stomp met liggend kruis
        ('3651', '3601'),  # Geel stomp met liggend kruis
        ('3652', '3601'),  # Geel stomp met liggend kruis
        ('3653', '3601'),  # Geel stomp met liggend kruis
        ('3654', '3601'),  # Geel stomp met liggend kruis
        ('3655', '3601'),  # Geel stomp met liggend kruis
        ('3656', '3601'),  # Geel stomp met liggend kruis
        ('3657', '3601'),  # Geel stomp met liggend kruis
        ('3658', '3601'),  # Geel stomp met liggend kruis
        ('3659', '3601'),  # Geel stomp met liggend kruis
        ('3660', '3601'),  # Geel stomp met liggend kruis
        ('3661', '3601'),  # Geel stomp met liggend kruis
        ('3662', '3601'),  # Geel stomp met liggend kruis
        ('3663', '3601'),  # Geel stomp met liggend kruis
        ('3664', '3601'),  # Geel stomp met liggend kruis
        ('3665', '3601'),  # Geel stomp met liggend kruis
        ('3666', '3601'),  # Geel stomp met liggend kruis
        ('3667', '3601'),  # Geel stomp met liggend kruis
        ('3668', '3601'),  # Geel stomp met liggend kruis
        ('3669', '3601'),  # Geel stomp met liggend kruis
        ('3670', '3601'),  # Geel stomp met liggend kruis
        ('3671', '3601'),  # Geel stomp met liggend kruis
        ('3672', '3601'),  # Geel stomp met liggend kruis
        ('3673', '3601'),  # Geel stomp met liggend kruis
        ('3674', '3601'),  # Geel stomp met liggend kruis
        ('3675', '3601'),  # Geel stomp met liggend kruis
        ('3676', '3601'),  # Geel stomp met liggend kruis
        ('3677', '3601'),  # Geel stomp met liggend kruis
        ('3678', '3601'),  # Geel stomp met liggend kruis
        ('3679', '3601'),  # Geel stomp met liggend kruis
        ('3680', '3601'),  # Geel stomp met liggend kruis
        ('3681', '3601'),  # Geel stomp met liggend kruis
        ('3682', '3601'),  # Geel stomp met liggend kruis
        ('3683', '3601'),  # Geel stomp met liggend kruis
        ('3684', '3601'),  # Geel stomp met liggend kruis
        ('3685', '3601'),  # Geel stomp met liggend kruis
        ('3701', '3701'),  # Geel stomp met geel licht
        ('3702', '3701'),  # Geel stomp met geel licht
        ('3703', '3701'),  # Geel stomp met geel licht
        ('3704', '3701'),  # Geel stomp met geel licht
        ('3705', '3701'),  # Geel stomp met geel licht
        ('3706', '3701'),  # Geel stomp met geel licht
        ('3707', '3701'),  # Geel stomp met geel licht
        ('3708', '3701'),  # Geel stomp met geel licht
        ('3709', '3701'),  # Geel stomp met geel licht
        ('3710', '3701'),  # Geel stomp met geel licht
        ('3711', '3701'),  # Geel stomp met geel licht
        ('3712', '3701'),  # Geel stomp met geel licht
        ('3713', '3701'),  # Geel stomp met geel licht
        ('3714', '3701'),  # Geel stomp met geel licht
        ('3715', '3701'),  # Geel stomp met geel licht
        ('3716', '3701'),  # Geel stomp met geel licht
        ('3717', '3701'),  # Geel stomp met geel licht
        ('3718', '3701'),  # Geel stomp met geel licht
        ('3719', '3701'),  # Geel stomp met geel licht
        ('3720', '3701'),  # Geel stomp met geel licht
        ('3721', '3701'),  # Geel stomp met geel licht
        ('3722', '3701'),  # Geel stomp met geel licht
        ('3723', '3701'),  # Geel stomp met geel licht
        ('3724', '3701'),  # Geel stomp met geel licht
        ('3725', '3701'),  # Geel stomp met geel licht
        ('3726', '3701'),  # Geel stomp met geel licht
        ('3727', '3701'),  # Geel stomp met geel licht
        ('3728', '3701'),  # Geel stomp met geel licht
        ('3729', '3701'),  # Geel stomp met geel licht
        ('3730', '3701'),  # Geel stomp met geel licht
        ('3731', '3701'),  # Geel stomp met geel licht
        ('3732', '3701'),  # Geel stomp met geel licht
        ('3733', '3701'),  # Geel stomp met geel licht
        ('3734', '3701'),  # Geel stomp met geel licht
        ('3735', '3701'),  # Geel stomp met geel licht
        ('3751', '3701'),  # Geel stomp met geel licht
        ('3752', '3701'),  # Geel stomp met geel licht
        ('3753', '3701'),  # Geel stomp met geel licht
        ('3754', '3701'),  # Geel stomp met geel licht
        ('3755', '3701'),  # Geel stomp met geel licht
        ('3756', '3701'),  # Geel stomp met geel licht
        ('3757', '3701'),  # Geel stomp met geel licht
        ('3758', '3701'),  # Geel stomp met geel licht
        ('3759', '3701'),  # Geel stomp met geel licht
        ('3760', '3701'),  # Geel stomp met geel licht
        ('3761', '3701'),  # Geel stomp met geel licht
        ('3762', '3701'),  # Geel stomp met geel licht
        ('3763', '3701'),  # Geel stomp met geel licht
        ('3764', '3701'),  # Geel stomp met geel licht
        ('3765', '3701'),  # Geel stomp met geel licht
        ('3766', '3701'),  # Geel stomp met geel licht
        ('3767', '3701'),  # Geel stomp met geel licht
        ('3768', '3701'),  # Geel stomp met geel licht
        ('3769', '3701'),  # Geel stomp met geel licht
        ('3770', '3701'),  # Geel stomp met geel licht
        ('3771', '3701'),  # Geel stomp met geel licht
        ('3772', '3701'),  # Geel stomp met geel licht
        ('3773', '3701'),  # Geel stomp met geel licht
        ('3774', '3701'),  # Geel stomp met geel licht
        ('3775', '3701'),  # Geel stomp met geel licht
        ('3776', '3701'),  # Geel stomp met geel licht
        ('3777', '3701'),  # Geel stomp met geel licht
        ('3778', '3701'),  # Geel stomp met geel licht
        ('3779', '3701'),  # Geel stomp met geel licht
        ('3780', '3701'),  # Geel stomp met geel licht
        ('3781', '3701'),  # Geel stomp met geel licht
        ('3782', '3701'),  # Geel stomp met geel licht
        ('3783', '3701'),  # Geel stomp met geel licht
        ('3784', '3701'),  # Geel stomp met geel licht
        ('3785', '3701'),  # Geel stomp met geel licht
        ('3801', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3802', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3803', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3804', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3805', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3806', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3807', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3808', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3809', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3810', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3811', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3812', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3813', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3814', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3815', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3816', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3817', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3818', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3819', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3820', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3821', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3822', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3823', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3824', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3825', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3826', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3827', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3828', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3829', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3830', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3831', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3832', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3833', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3834', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3835', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3851', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3852', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3853', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3854', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3855', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3856', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3857', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3858', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3859', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3860', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3861', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3862', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3863', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3864', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3865', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3866', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3867', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3868', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3869', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3870', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3871', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3872', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3873', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3874', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3875', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3876', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3877', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3878', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3879', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3880', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3881', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3882', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3883', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3884', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('3885', '3801'),  # Geel stomp met liggend kruis en geel licht
        ('4001', '4001'),  # Geel bol
        ('4002', '4001'),  # Geel bol
        ('4003', '4001'),  # Geel bol
        ('4004', '4001'),  # Geel bol
        ('4005', '4001'),  # Geel bol
        ('4006', '4001'),  # Geel bol
        ('4007', '4001'),  # Geel bol
        ('4008', '4001'),  # Geel bol
        ('4009', '4001'),  # Geel bol
        ('4010', '4001'),  # Geel bol
        ('4011', '4001'),  # Geel bol
        ('4012', '4001'),  # Geel bol
        ('4013', '4001'),  # Geel bol
        ('4014', '4001'),  # Geel bol
        ('4015', '4001'),  # Geel bol
        ('4016', '4001'),  # Geel bol
        ('4017', '4001'),  # Geel bol
        ('4018', '4001'),  # Geel bol
        ('4019', '4001'),  # Geel bol
        ('4020', '4001'),  # Geel bol
        ('4021', '4001'),  # Geel bol
        ('4022', '4001'),  # Geel bol
        ('4023', '4001'),  # Geel bol
        ('4024', '4001'),  # Geel bol
        ('4025', '4001'),  # Geel bol
        ('4026', '4001'),  # Geel bol
        ('4027', '4001'),  # Geel bol
        ('4028', '4001'),  # Geel bol
        ('4029', '4001'),  # Geel bol
        ('4030', '4001'),  # Geel bol
        ('4031', '4001'),  # Geel bol
        ('4032', '4001'),  # Geel bol
        ('4033', '4001'),  # Geel bol
        ('4034', '4001'),  # Geel bol
        ('4035', '4001'),  # Geel bol
        ('4051', '4001'),  # Geel bol
        ('4052', '4001'),  # Geel bol
        ('4053', '4001'),  # Geel bol
        ('4054', '4001'),  # Geel bol
        ('4055', '4001'),  # Geel bol
        ('4056', '4001'),  # Geel bol
        ('4057', '4001'),  # Geel bol
        ('4058', '4001'),  # Geel bol
        ('4059', '4001'),  # Geel bol
        ('4060', '4001'),  # Geel bol
        ('4061', '4001'),  # Geel bol
        ('4062', '4001'),  # Geel bol
        ('4063', '4001'),  # Geel bol
        ('4064', '4001'),  # Geel bol
        ('4065', '4001'),  # Geel bol
        ('4066', '4001'),  # Geel bol
        ('4067', '4001'),  # Geel bol
        ('4068', '4001'),  # Geel bol
        ('4069', '4001'),  # Geel bol
        ('4070', '4001'),  # Geel bol
        ('4071', '4001'),  # Geel bol
        ('4072', '4001'),  # Geel bol
        ('4073', '4001'),  # Geel bol
        ('4074', '4001'),  # Geel bol
        ('4075', '4001'),  # Geel bol
        ('4076', '4001'),  # Geel bol
        ('4077', '4001'),  # Geel bol
        ('4078', '4001'),  # Geel bol
        ('4079', '4001'),  # Geel bol
        ('4080', '4001'),  # Geel bol
        ('4081', '4001'),  # Geel bol
        ('4082', '4001'),  # Geel bol
        ('4083', '4001'),  # Geel bol
        ('4084', '4001'),  # Geel bol
        ('4085', '4001'),  # Geel bol
        ('4101', '4101'),  # Geel bol met liggend kruis
        ('4102', '4101'),  # Geel bol met liggend kruis
        ('4103', '4101'),  # Geel bol met liggend kruis
        ('4104', '4101'),  # Geel bol met liggend kruis
        ('4105', '4101'),  # Geel bol met liggend kruis
        ('4106', '4101'),  # Geel bol met liggend kruis
        ('4107', '4101'),  # Geel bol met liggend kruis
        ('4108', '4101'),  # Geel bol met liggend kruis
        ('4109', '4101'),  # Geel bol met liggend kruis
        ('4110', '4101'),  # Geel bol met liggend kruis
        ('4111', '4101'),  # Geel bol met liggend kruis
        ('4112', '4101'),  # Geel bol met liggend kruis
        ('4113', '4101'),  # Geel bol met liggend kruis
        ('4114', '4101'),  # Geel bol met liggend kruis
        ('4115', '4101'),  # Geel bol met liggend kruis
        ('4116', '4101'),  # Geel bol met liggend kruis
        ('4117', '4101'),  # Geel bol met liggend kruis
        ('4118', '4101'),  # Geel bol met liggend kruis
        ('4119', '4101'),  # Geel bol met liggend kruis
        ('4120', '4101'),  # Geel bol met liggend kruis
        ('4121', '4101'),  # Geel bol met liggend kruis
        ('4122', '4101'),  # Geel bol met liggend kruis
        ('4123', '4101'),  # Geel bol met liggend kruis
        ('4124', '4101'),  # Geel bol met liggend kruis
        ('4125', '4101'),  # Geel bol met liggend kruis
        ('4126', '4101'),  # Geel bol met liggend kruis
        ('4127', '4101'),  # Geel bol met liggend kruis
        ('4128', '4101'),  # Geel bol met liggend kruis
        ('4129', '4101'),  # Geel bol met liggend kruis
        ('4130', '4101'),  # Geel bol met liggend kruis
        ('4131', '4101'),  # Geel bol met liggend kruis
        ('4132', '4101'),  # Geel bol met liggend kruis
        ('4133', '4101'),  # Geel bol met liggend kruis
        ('4134', '4101'),  # Geel bol met liggend kruis
        ('4135', '4101'),  # Geel bol met liggend kruis
        ('4151', '4101'),  # Geel bol met liggend kruis
        ('4152', '4101'),  # Geel bol met liggend kruis
        ('4153', '4101'),  # Geel bol met liggend kruis
        ('4154', '4101'),  # Geel bol met liggend kruis
        ('4155', '4101'),  # Geel bol met liggend kruis
        ('4156', '4101'),  # Geel bol met liggend kruis
        ('4157', '4101'),  # Geel bol met liggend kruis
        ('4158', '4101'),  # Geel bol met liggend kruis
        ('4159', '4101'),  # Geel bol met liggend kruis
        ('4160', '4101'),  # Geel bol met liggend kruis
        ('4161', '4101'),  # Geel bol met liggend kruis
        ('4162', '4101'),  # Geel bol met liggend kruis
        ('4163', '4101'),  # Geel bol met liggend kruis
        ('4164', '4101'),  # Geel bol met liggend kruis
        ('4165', '4101'),  # Geel bol met liggend kruis
        ('4166', '4101'),  # Geel bol met liggend kruis
        ('4167', '4101'),  # Geel bol met liggend kruis
        ('4168', '4101'),  # Geel bol met liggend kruis
        ('4169', '4101'),  # Geel bol met liggend kruis
        ('4170', '4101'),  # Geel bol met liggend kruis
        ('4171', '4101'),  # Geel bol met liggend kruis
        ('4172', '4101'),  # Geel bol met liggend kruis
        ('4173', '4101'),  # Geel bol met liggend kruis
        ('4174', '4101'),  # Geel bol met liggend kruis
        ('4175', '4101'),  # Geel bol met liggend kruis
        ('4176', '4101'),  # Geel bol met liggend kruis
        ('4177', '4101'),  # Geel bol met liggend kruis
        ('4178', '4101'),  # Geel bol met liggend kruis
        ('4179', '4101'),  # Geel bol met liggend kruis
        ('4180', '4101'),  # Geel bol met liggend kruis
        ('4181', '4101'),  # Geel bol met liggend kruis
        ('4182', '4101'),  # Geel bol met liggend kruis
        ('4183', '4101'),  # Geel bol met liggend kruis
        ('4184', '4101'),  # Geel bol met liggend kruis
        ('4185', '4101'),  # Geel bol met liggend kruis
        ('4201', '4201'),  # Geel bol met geel licht
        ('4202', '4201'),  # Geel bol met geel licht
        ('4203', '4201'),  # Geel bol met geel licht
        ('4204', '4201'),  # Geel bol met geel licht
        ('4205', '4201'),  # Geel bol met geel licht
        ('4206', '4201'),  # Geel bol met geel licht
        ('4207', '4201'),  # Geel bol met geel licht
        ('4208', '4201'),  # Geel bol met geel licht
        ('4209', '4201'),  # Geel bol met geel licht
        ('4210', '4201'),  # Geel bol met geel licht
        ('4211', '4201'),  # Geel bol met geel licht
        ('4212', '4201'),  # Geel bol met geel licht
        ('4213', '4201'),  # Geel bol met geel licht
        ('4214', '4201'),  # Geel bol met geel licht
        ('4215', '4201'),  # Geel bol met geel licht
        ('4216', '4201'),  # Geel bol met geel licht
        ('4217', '4201'),  # Geel bol met geel licht
        ('4218', '4201'),  # Geel bol met geel licht
        ('4219', '4201'),  # Geel bol met geel licht
        ('4220', '4201'),  # Geel bol met geel licht
        ('4221', '4201'),  # Geel bol met geel licht
        ('4222', '4201'),  # Geel bol met geel licht
        ('4223', '4201'),  # Geel bol met geel licht
        ('4224', '4201'),  # Geel bol met geel licht
        ('4225', '4201'),  # Geel bol met geel licht
        ('4226', '4201'),  # Geel bol met geel licht
        ('4227', '4201'),  # Geel bol met geel licht
        ('4228', '4201'),  # Geel bol met geel licht
        ('4229', '4201'),  # Geel bol met geel licht
        ('4230', '4201'),  # Geel bol met geel licht
        ('4231', '4201'),  # Geel bol met geel licht
        ('4232', '4201'),  # Geel bol met geel licht
        ('4233', '4201'),  # Geel bol met geel licht
        ('4234', '4201'),  # Geel bol met geel licht
        ('4235', '4201'),  # Geel bol met geel licht
        ('4251', '4201'),  # Geel bol met geel licht
        ('4252', '4201'),  # Geel bol met geel licht
        ('4253', '4201'),  # Geel bol met geel licht
        ('4254', '4201'),  # Geel bol met geel licht
        ('4255', '4201'),  # Geel bol met geel licht
        ('4256', '4201'),  # Geel bol met geel licht
        ('4257', '4201'),  # Geel bol met geel licht
        ('4258', '4201'),  # Geel bol met geel licht
        ('4259', '4201'),  # Geel bol met geel licht
        ('4260', '4201'),  # Geel bol met geel licht
        ('4261', '4201'),  # Geel bol met geel licht
        ('4262', '4201'),  # Geel bol met geel licht
        ('4263', '4201'),  # Geel bol met geel licht
        ('4264', '4201'),  # Geel bol met geel licht
        ('4265', '4201'),  # Geel bol met geel licht
        ('4266', '4201'),  # Geel bol met geel licht
        ('4267', '4201'),  # Geel bol met geel licht
        ('4268', '4201'),  # Geel bol met geel licht
        ('4269', '4201'),  # Geel bol met geel licht
        ('4270', '4201'),  # Geel bol met geel licht
        ('4271', '4201'),  # Geel bol met geel licht
        ('4272', '4201'),  # Geel bol met geel licht
        ('4273', '4201'),  # Geel bol met geel licht
        ('4274', '4201'),  # Geel bol met geel licht
        ('4275', '4201'),  # Geel bol met geel licht
        ('4276', '4201'),  # Geel bol met geel licht
        ('4277', '4201'),  # Geel bol met geel licht
        ('4278', '4201'),  # Geel bol met geel licht
        ('4279', '4201'),  # Geel bol met geel licht
        ('4280', '4201'),  # Geel bol met geel licht
        ('4281', '4201'),  # Geel bol met geel licht
        ('4282', '4201'),  # Geel bol met geel licht
        ('4283', '4201'),  # Geel bol met geel licht
        ('4284', '4201'),  # Geel bol met geel licht
        ('4285', '4201'),  # Geel bol met geel licht
        ('4301', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4302', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4303', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4304', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4305', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4306', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4307', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4308', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4309', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4310', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4311', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4312', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4313', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4314', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4315', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4316', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4317', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4318', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4319', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4320', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4321', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4322', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4323', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4324', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4325', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4326', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4327', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4328', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4329', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4330', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4331', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4332', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4333', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4334', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4335', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4351', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4352', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4353', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4354', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4355', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4356', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4357', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4358', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4359', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4360', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4361', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4362', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4363', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4364', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4365', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4366', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4367', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4368', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4369', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4370', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4371', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4372', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4373', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4374', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4375', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4376', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4377', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4378', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4379', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4380', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4381', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4382', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4383', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4384', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4385', '4301'),  # Geel bol met liggend kruis en geel licht
        ('4500', '4500'),  # Geel pilaar
        ('4501', '4500'),  # Geel pilaar
        ('4502', '4500'),  # Geel pilaar
        ('4503', '4500'),  # Geel pilaar
        ('4504', '4500'),  # Geel pilaar
        ('4505', '4500'),  # Geel pilaar
        ('4506', '4500'),  # Geel pilaar
        ('4507', '4500'),  # Geel pilaar
        ('4508', '4500'),  # Geel pilaar
        ('4509', '4500'),  # Geel pilaar
        ('4510', '4500'),  # Geel pilaar
        ('4511', '4500'),  # Geel pilaar
        ('4512', '4500'),  # Geel pilaar
        ('4513', '4500'),  # Geel pilaar
        ('4514', '4500'),  # Geel pilaar
        ('4515', '4500'),  # Geel pilaar
        ('4516', '4500'),  # Geel pilaar
        ('4517', '4500'),  # Geel pilaar
        ('4518', '4500'),  # Geel pilaar
        ('4519', '4500'),  # Geel pilaar
        ('4520', '4500'),  # Geel pilaar
        ('4521', '4500'),  # Geel pilaar
        ('4522', '4500'),  # Geel pilaar
        ('4523', '4500'),  # Geel pilaar
        ('4524', '4500'),  # Geel pilaar
        ('4525', '4500'),  # Geel pilaar
        ('4526', '4500'),  # Geel pilaar
        ('4527', '4500'),  # Geel pilaar
        ('4528', '4500'),  # Geel pilaar
        ('4529', '4500'),  # Geel pilaar
        ('4530', '4500'),  # Geel pilaar
        ('4531', '4500'),  # Geel pilaar
        ('4532', '4500'),  # Geel pilaar
        ('4533', '4500'),  # Geel pilaar
        ('4534', '4500'),  # Geel pilaar
        ('4535', '4500'),  # Geel pilaar
        ('4550', '4500'),  # Geel pilaar
        ('4551', '4500'),  # Geel pilaar
        ('4552', '4500'),  # Geel pilaar
        ('4553', '4500'),  # Geel pilaar
        ('4554', '4500'),  # Geel pilaar
        ('4555', '4500'),  # Geel pilaar
        ('4556', '4500'),  # Geel pilaar
        ('4557', '4500'),  # Geel pilaar
        ('4558', '4500'),  # Geel pilaar
        ('4559', '4500'),  # Geel pilaar
        ('4560', '4500'),  # Geel pilaar
        ('4561', '4500'),  # Geel pilaar
        ('4562', '4500'),  # Geel pilaar
        ('4563', '4500'),  # Geel pilaar
        ('4564', '4500'),  # Geel pilaar
        ('4565', '4500'),  # Geel pilaar
        ('4566', '4500'),  # Geel pilaar
        ('4567', '4500'),  # Geel pilaar
        ('4568', '4500'),  # Geel pilaar
        ('4569', '4500'),  # Geel pilaar
        ('4570', '4500'),  # Geel pilaar
        ('4571', '4500'),  # Geel pilaar
        ('4572', '4500'),  # Geel pilaar
        ('4573', '4500'),  # Geel pilaar
        ('4574', '4500'),  # Geel pilaar
        ('4575', '4500'),  # Geel pilaar
        ('4576', '4500'),  # Geel pilaar
        ('4577', '4500'),  # Geel pilaar
        ('4578', '4500'),  # Geel pilaar
        ('4579', '4500'),  # Geel pilaar
        ('4580', '4500'),  # Geel pilaar
        ('4581', '4500'),  # Geel pilaar
        ('4582', '4500'),  # Geel pilaar
        ('4583', '4500'),  # Geel pilaar
        ('4584', '4500'),  # Geel pilaar
        ('4585', '4500'),  # Geel pilaar
        ('4600', '4600'),  # Geel pilaar met liggend kruis
        ('4601', '4600'),  # Geel pilaar met liggend kruis
        ('4602', '4600'),  # Geel pilaar met liggend kruis
        ('4603', '4600'),  # Geel pilaar met liggend kruis
        ('4604', '4600'),  # Geel pilaar met liggend kruis
        ('4605', '4600'),  # Geel pilaar met liggend kruis
        ('4606', '4600'),  # Geel pilaar met liggend kruis
        ('4607', '4600'),  # Geel pilaar met liggend kruis
        ('4608', '4600'),  # Geel pilaar met liggend kruis
        ('4609', '4600'),  # Geel pilaar met liggend kruis
        ('4610', '4600'),  # Geel pilaar met liggend kruis
        ('4611', '4600'),  # Geel pilaar met liggend kruis
        ('4612', '4600'),  # Geel pilaar met liggend kruis
        ('4613', '4600'),  # Geel pilaar met liggend kruis
        ('4614', '4600'),  # Geel pilaar met liggend kruis
        ('4615', '4600'),  # Geel pilaar met liggend kruis
        ('4616', '4600'),  # Geel pilaar met liggend kruis
        ('4617', '4600'),  # Geel pilaar met liggend kruis
        ('4618', '4600'),  # Geel pilaar met liggend kruis
        ('4619', '4600'),  # Geel pilaar met liggend kruis
        ('4620', '4600'),  # Geel pilaar met liggend kruis
        ('4621', '4600'),  # Geel pilaar met liggend kruis
        ('4622', '4600'),  # Geel pilaar met liggend kruis
        ('4623', '4600'),  # Geel pilaar met liggend kruis
        ('4624', '4600'),  # Geel pilaar met liggend kruis
        ('4625', '4600'),  # Geel pilaar met liggend kruis
        ('4626', '4600'),  # Geel pilaar met liggend kruis
        ('4627', '4600'),  # Geel pilaar met liggend kruis
        ('4628', '4600'),  # Geel pilaar met liggend kruis
        ('4629', '4600'),  # Geel pilaar met liggend kruis
        ('4630', '4600'),  # Geel pilaar met liggend kruis
        ('4631', '4600'),  # Geel pilaar met liggend kruis
        ('4632', '4600'),  # Geel pilaar met liggend kruis
        ('4633', '4600'),  # Geel pilaar met liggend kruis
        ('4634', '4600'),  # Geel pilaar met liggend kruis
        ('4635', '4600'),  # Geel pilaar met liggend kruis
        ('4650', '4600'),  # Geel pilaar met liggend kruis
        ('4651', '4600'),  # Geel pilaar met liggend kruis
        ('4652', '4600'),  # Geel pilaar met liggend kruis
        ('4653', '4600'),  # Geel pilaar met liggend kruis
        ('4654', '4600'),  # Geel pilaar met liggend kruis
        ('4655', '4600'),  # Geel pilaar met liggend kruis
        ('4656', '4600'),  # Geel pilaar met liggend kruis
        ('4657', '4600'),  # Geel pilaar met liggend kruis
        ('4658', '4600'),  # Geel pilaar met liggend kruis
        ('4659', '4600'),  # Geel pilaar met liggend kruis
        ('4660', '4600'),  # Geel pilaar met liggend kruis
        ('4661', '4600'),  # Geel pilaar met liggend kruis
        ('4662', '4600'),  # Geel pilaar met liggend kruis
        ('4663', '4600'),  # Geel pilaar met liggend kruis
        ('4664', '4600'),  # Geel pilaar met liggend kruis
        ('4665', '4600'),  # Geel pilaar met liggend kruis
        ('4666', '4600'),  # Geel pilaar met liggend kruis
        ('4667', '4600'),  # Geel pilaar met liggend kruis
        ('4668', '4600'),  # Geel pilaar met liggend kruis
        ('4669', '4600'),  # Geel pilaar met liggend kruis
        ('4670', '4600'),  # Geel pilaar met liggend kruis
        ('4671', '4600'),  # Geel pilaar met liggend kruis
        ('4672', '4600'),  # Geel pilaar met liggend kruis
        ('4673', '4600'),  # Geel pilaar met liggend kruis
        ('4674', '4600'),  # Geel pilaar met liggend kruis
        ('4675', '4600'),  # Geel pilaar met liggend kruis
        ('4676', '4600'),  # Geel pilaar met liggend kruis
        ('4677', '4600'),  # Geel pilaar met liggend kruis
        ('4678', '4600'),  # Geel pilaar met liggend kruis
        ('4679', '4600'),  # Geel pilaar met liggend kruis
        ('4680', '4600'),  # Geel pilaar met liggend kruis
        ('4681', '4600'),  # Geel pilaar met liggend kruis
        ('4682', '4600'),  # Geel pilaar met liggend kruis
        ('4683', '4600'),  # Geel pilaar met liggend kruis
        ('4684', '4600'),  # Geel pilaar met liggend kruis
        ('4685', '4600'),  # Geel pilaar met liggend kruis
        ('4701', '4701'),  # Geel pilaar met geel licht
        ('4702', '4701'),  # Geel pilaar met geel licht
        ('4703', '4701'),  # Geel pilaar met geel licht
        ('4704', '4701'),  # Geel pilaar met geel licht
        ('4705', '4701'),  # Geel pilaar met geel licht
        ('4706', '4701'),  # Geel pilaar met geel licht
        ('4707', '4701'),  # Geel pilaar met geel licht
        ('4708', '4701'),  # Geel pilaar met geel licht
        ('4709', '4701'),  # Geel pilaar met geel licht
        ('4710', '4701'),  # Geel pilaar met geel licht
        ('4711', '4701'),  # Geel pilaar met geel licht
        ('4712', '4701'),  # Geel pilaar met geel licht
        ('4713', '4701'),  # Geel pilaar met geel licht
        ('4714', '4701'),  # Geel pilaar met geel licht
        ('4715', '4701'),  # Geel pilaar met geel licht
        ('4716', '4701'),  # Geel pilaar met geel licht
        ('4717', '4701'),  # Geel pilaar met geel licht
        ('4718', '4701'),  # Geel pilaar met geel licht
        ('4719', '4701'),  # Geel pilaar met geel licht
        ('4720', '4701'),  # Geel pilaar met geel licht
        ('4721', '4701'),  # Geel pilaar met geel licht
        ('4722', '4701'),  # Geel pilaar met geel licht
        ('4723', '4701'),  # Geel pilaar met geel licht
        ('4724', '4701'),  # Geel pilaar met geel licht
        ('4725', '4701'),  # Geel pilaar met geel licht
        ('4726', '4701'),  # Geel pilaar met geel licht
        ('4727', '4701'),  # Geel pilaar met geel licht
        ('4728', '4701'),  # Geel pilaar met geel licht
        ('4729', '4701'),  # Geel pilaar met geel licht
        ('4730', '4701'),  # Geel pilaar met geel licht
        ('4731', '4701'),  # Geel pilaar met geel licht
        ('4732', '4701'),  # Geel pilaar met geel licht
        ('4733', '4701'),  # Geel pilaar met geel licht
        ('4734', '4701'),  # Geel pilaar met geel licht
        ('4735', '4701'),  # Geel pilaar met geel licht
        ('4751', '4701'),  # Geel pilaar met geel licht
        ('4752', '4701'),  # Geel pilaar met geel licht
        ('4753', '4701'),  # Geel pilaar met geel licht
        ('4754', '4701'),  # Geel pilaar met geel licht
        ('4755', '4701'),  # Geel pilaar met geel licht
        ('4756', '4701'),  # Geel pilaar met geel licht
        ('4757', '4701'),  # Geel pilaar met geel licht
        ('4758', '4701'),  # Geel pilaar met geel licht
        ('4759', '4701'),  # Geel pilaar met geel licht
        ('4760', '4701'),  # Geel pilaar met geel licht
        ('4761', '4701'),  # Geel pilaar met geel licht
        ('4762', '4701'),  # Geel pilaar met geel licht
        ('4763', '4701'),  # Geel pilaar met geel licht
        ('4764', '4701'),  # Geel pilaar met geel licht
        ('4765', '4701'),  # Geel pilaar met geel licht
        ('4766', '4701'),  # Geel pilaar met geel licht
        ('4767', '4701'),  # Geel pilaar met geel licht
        ('4768', '4701'),  # Geel pilaar met geel licht
        ('4769', '4701'),  # Geel pilaar met geel licht
        ('4770', '4701'),  # Geel pilaar met geel licht
        ('4771', '4701'),  # Geel pilaar met geel licht
        ('4772', '4701'),  # Geel pilaar met geel licht
        ('4773', '4701'),  # Geel pilaar met geel licht
        ('4774', '4701'),  # Geel pilaar met geel licht
        ('4775', '4701'),  # Geel pilaar met geel licht
        ('4776', '4701'),  # Geel pilaar met geel licht
        ('4777', '4701'),  # Geel pilaar met geel licht
        ('4778', '4701'),  # Geel pilaar met geel licht
        ('4779', '4701'),  # Geel pilaar met geel licht
        ('4780', '4701'),  # Geel pilaar met geel licht
        ('4781', '4701'),  # Geel pilaar met geel licht
        ('4782', '4701'),  # Geel pilaar met geel licht
        ('4783', '4701'),  # Geel pilaar met geel licht
        ('4784', '4701'),  # Geel pilaar met geel licht
        ('4785', '4701'),  # Geel pilaar met geel licht
        ('4801', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4802', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4803', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4804', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4805', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4806', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4807', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4808', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4809', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4810', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4811', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4812', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4813', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4814', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4815', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4816', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4817', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4818', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4819', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4820', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4821', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4822', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4823', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4824', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4825', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4826', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4827', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4828', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4829', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4830', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4831', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4832', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4833', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4834', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4835', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4851', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4852', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4853', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4854', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4855', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4856', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4857', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4858', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4859', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4860', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4861', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4862', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4863', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4864', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4865', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4866', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4867', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4868', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4869', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4870', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4871', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4872', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4873', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4874', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4875', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4876', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4877', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4878', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4879', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4880', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4881', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4882', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4883', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4884', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('4885', '4801'),  # Geel pilaar met liggens kruis en geel licht
        ('5000', '5000'),  # Geel spar
        ('5001', '5000'),  # Geel spar
        ('5002', '5000'),  # Geel spar
        ('5003', '5000'),  # Geel spar
        ('5004', '5000'),  # Geel spar
        ('5005', '5000'),  # Geel spar
        ('5006', '5000'),  # Geel spar
        ('5007', '5000'),  # Geel spar
        ('5008', '5000'),  # Geel spar
        ('5009', '5000'),  # Geel spar
        ('5010', '5000'),  # Geel spar
        ('5011', '5000'),  # Geel spar
        ('5012', '5000'),  # Geel spar
        ('5013', '5000'),  # Geel spar
        ('5014', '5000'),  # Geel spar
        ('5015', '5000'),  # Geel spar
        ('5016', '5000'),  # Geel spar
        ('5017', '5000'),  # Geel spar
        ('5018', '5000'),  # Geel spar
        ('5019', '5000'),  # Geel spar
        ('5020', '5000'),  # Geel spar
        ('5021', '5000'),  # Geel spar
        ('5022', '5000'),  # Geel spar
        ('5023', '5000'),  # Geel spar
        ('5024', '5000'),  # Geel spar
        ('5025', '5000'),  # Geel spar
        ('5026', '5000'),  # Geel spar
        ('5027', '5000'),  # Geel spar
        ('5028', '5000'),  # Geel spar
        ('5029', '5000'),  # Geel spar
        ('5030', '5000'),  # Geel spar
        ('5031', '5000'),  # Geel spar
        ('5032', '5000'),  # Geel spar
        ('5033', '5000'),  # Geel spar
        ('5034', '5000'),  # Geel spar
        ('5035', '5000'),  # Geel spar
        ('5051', '5000'),  # Geel spar
        ('5052', '5000'),  # Geel spar
        ('5053', '5000'),  # Geel spar
        ('5054', '5000'),  # Geel spar
        ('5055', '5000'),  # Geel spar
        ('5056', '5000'),  # Geel spar
        ('5057', '5000'),  # Geel spar
        ('5058', '5000'),  # Geel spar
        ('5059', '5000'),  # Geel spar
        ('5060', '5000'),  # Geel spar
        ('5061', '5000'),  # Geel spar
        ('5062', '5000'),  # Geel spar
        ('5063', '5000'),  # Geel spar
        ('5064', '5000'),  # Geel spar
        ('5065', '5000'),  # Geel spar
        ('5066', '5000'),  # Geel spar
        ('5067', '5000'),  # Geel spar
        ('5068', '5000'),  # Geel spar
        ('5069', '5000'),  # Geel spar
        ('5070', '5000'),  # Geel spar
        ('5071', '5000'),  # Geel spar
        ('5072', '5000'),  # Geel spar
        ('5073', '5000'),  # Geel spar
        ('5074', '5000'),  # Geel spar
        ('5075', '5000'),  # Geel spar
        ('5076', '5000'),  # Geel spar
        ('5077', '5000'),  # Geel spar
        ('5078', '5000'),  # Geel spar
        ('5079', '5000'),  # Geel spar
        ('5080', '5000'),  # Geel spar
        ('5081', '5000'),  # Geel spar
        ('5082', '5000'),  # Geel spar
        ('5083', '5000'),  # Geel spar
        ('5084', '5000'),  # Geel spar
        ('5085', '5000'),  # Geel spar
        ('5101', '5101'),  # Geel spar met liggend kruis
        ('5102', '5101'),  # Geel spar met liggend kruis
        ('5103', '5101'),  # Geel spar met liggend kruis
        ('5104', '5101'),  # Geel spar met liggend kruis
        ('5105', '5101'),  # Geel spar met liggend kruis
        ('5106', '5101'),  # Geel spar met liggend kruis
        ('5107', '5101'),  # Geel spar met liggend kruis
        ('5108', '5101'),  # Geel spar met liggend kruis
        ('5109', '5101'),  # Geel spar met liggend kruis
        ('5110', '5101'),  # Geel spar met liggend kruis
        ('5111', '5101'),  # Geel spar met liggend kruis
        ('5112', '5101'),  # Geel spar met liggend kruis
        ('5113', '5101'),  # Geel spar met liggend kruis
        ('5114', '5101'),  # Geel spar met liggend kruis
        ('5115', '5101'),  # Geel spar met liggend kruis
        ('5116', '5101'),  # Geel spar met liggend kruis
        ('5117', '5101'),  # Geel spar met liggend kruis
        ('5118', '5101'),  # Geel spar met liggend kruis
        ('5119', '5101'),  # Geel spar met liggend kruis
        ('5120', '5101'),  # Geel spar met liggend kruis
        ('5121', '5101'),  # Geel spar met liggend kruis
        ('5122', '5101'),  # Geel spar met liggend kruis
        ('5123', '5101'),  # Geel spar met liggend kruis
        ('5124', '5101'),  # Geel spar met liggend kruis
        ('5125', '5101'),  # Geel spar met liggend kruis
        ('5126', '5101'),  # Geel spar met liggend kruis
        ('5127', '5101'),  # Geel spar met liggend kruis
        ('5128', '5101'),  # Geel spar met liggend kruis
        ('5129', '5101'),  # Geel spar met liggend kruis
        ('5130', '5101'),  # Geel spar met liggend kruis
        ('5131', '5101'),  # Geel spar met liggend kruis
        ('5132', '5101'),  # Geel spar met liggend kruis
        ('5133', '5101'),  # Geel spar met liggend kruis
        ('5134', '5101'),  # Geel spar met liggend kruis
        ('5135', '5101'),  # Geel spar met liggend kruis
        ('5151', '5101'),  # Geel spar met liggend kruis
        ('5152', '5101'),  # Geel spar met liggend kruis
        ('5153', '5101'),  # Geel spar met liggend kruis
        ('5154', '5101'),  # Geel spar met liggend kruis
        ('5155', '5101'),  # Geel spar met liggend kruis
        ('5156', '5101'),  # Geel spar met liggend kruis
        ('5157', '5101'),  # Geel spar met liggend kruis
        ('5158', '5101'),  # Geel spar met liggend kruis
        ('5159', '5101'),  # Geel spar met liggend kruis
        ('5160', '5101'),  # Geel spar met liggend kruis
        ('5161', '5101'),  # Geel spar met liggend kruis
        ('5162', '5101'),  # Geel spar met liggend kruis
        ('5163', '5101'),  # Geel spar met liggend kruis
        ('5164', '5101'),  # Geel spar met liggend kruis
        ('5165', '5101'),  # Geel spar met liggend kruis
        ('5166', '5101'),  # Geel spar met liggend kruis
        ('5167', '5101'),  # Geel spar met liggend kruis
        ('5168', '5101'),  # Geel spar met liggend kruis
        ('5169', '5101'),  # Geel spar met liggend kruis
        ('5170', '5101'),  # Geel spar met liggend kruis
        ('5171', '5101'),  # Geel spar met liggend kruis
        ('5172', '5101'),  # Geel spar met liggend kruis
        ('5173', '5101'),  # Geel spar met liggend kruis
        ('5174', '5101'),  # Geel spar met liggend kruis
        ('5175', '5101'),  # Geel spar met liggend kruis
        ('5176', '5101'),  # Geel spar met liggend kruis
        ('5177', '5101'),  # Geel spar met liggend kruis
        ('5178', '5101'),  # Geel spar met liggend kruis
        ('5179', '5101'),  # Geel spar met liggend kruis
        ('5180', '5101'),  # Geel spar met liggend kruis
        ('5181', '5101'),  # Geel spar met liggend kruis
        ('5182', '5101'),  # Geel spar met liggend kruis
        ('5183', '5101'),  # Geel spar met liggend kruis
        ('5184', '5101'),  # Geel spar met liggend kruis
        ('5185', '5101'),  # Geel spar met liggend kruis
        ('5201', '5201'),  # Geel spar met geel licht
        ('5202', '5201'),  # Geel spar met geel licht
        ('5203', '5201'),  # Geel spar met geel licht
        ('5204', '5201'),  # Geel spar met geel licht
        ('5205', '5201'),  # Geel spar met geel licht
        ('5206', '5201'),  # Geel spar met geel licht
        ('5207', '5201'),  # Geel spar met geel licht
        ('5208', '5201'),  # Geel spar met geel licht
        ('5209', '5201'),  # Geel spar met geel licht
        ('5210', '5201'),  # Geel spar met geel licht
        ('5211', '5201'),  # Geel spar met geel licht
        ('5212', '5201'),  # Geel spar met geel licht
        ('5213', '5201'),  # Geel spar met geel licht
        ('5214', '5201'),  # Geel spar met geel licht
        ('5215', '5201'),  # Geel spar met geel licht
        ('5216', '5201'),  # Geel spar met geel licht
        ('5217', '5201'),  # Geel spar met geel licht
        ('5218', '5201'),  # Geel spar met geel licht
        ('5219', '5201'),  # Geel spar met geel licht
        ('5220', '5201'),  # Geel spar met geel licht
        ('5221', '5201'),  # Geel spar met geel licht
        ('5222', '5201'),  # Geel spar met geel licht
        ('5223', '5201'),  # Geel spar met geel licht
        ('5224', '5201'),  # Geel spar met geel licht
        ('5225', '5201'),  # Geel spar met geel licht
        ('5226', '5201'),  # Geel spar met geel licht
        ('5227', '5201'),  # Geel spar met geel licht
        ('5228', '5201'),  # Geel spar met geel licht
        ('5229', '5201'),  # Geel spar met geel licht
        ('5230', '5201'),  # Geel spar met geel licht
        ('5231', '5201'),  # Geel spar met geel licht
        ('5232', '5201'),  # Geel spar met geel licht
        ('5233', '5201'),  # Geel spar met geel licht
        ('5234', '5201'),  # Geel spar met geel licht
        ('5235', '5201'),  # Geel spar met geel licht
        ('5251', '5201'),  # Geel spar met geel licht
        ('5252', '5201'),  # Geel spar met geel licht
        ('5253', '5201'),  # Geel spar met geel licht
        ('5254', '5201'),  # Geel spar met geel licht
        ('5255', '5201'),  # Geel spar met geel licht
        ('5256', '5201'),  # Geel spar met geel licht
        ('5257', '5201'),  # Geel spar met geel licht
        ('5258', '5201'),  # Geel spar met geel licht
        ('5259', '5201'),  # Geel spar met geel licht
        ('5260', '5201'),  # Geel spar met geel licht
        ('5261', '5201'),  # Geel spar met geel licht
        ('5262', '5201'),  # Geel spar met geel licht
        ('5263', '5201'),  # Geel spar met geel licht
        ('5264', '5201'),  # Geel spar met geel licht
        ('5265', '5201'),  # Geel spar met geel licht
        ('5266', '5201'),  # Geel spar met geel licht
        ('5267', '5201'),  # Geel spar met geel licht
        ('5268', '5201'),  # Geel spar met geel licht
        ('5269', '5201'),  # Geel spar met geel licht
        ('5270', '5201'),  # Geel spar met geel licht
        ('5271', '5201'),  # Geel spar met geel licht
        ('5272', '5201'),  # Geel spar met geel licht
        ('5273', '5201'),  # Geel spar met geel licht
        ('5274', '5201'),  # Geel spar met geel licht
        ('5275', '5201'),  # Geel spar met geel licht
        ('5276', '5201'),  # Geel spar met geel licht
        ('5277', '5201'),  # Geel spar met geel licht
        ('5278', '5201'),  # Geel spar met geel licht
        ('5279', '5201'),  # Geel spar met geel licht
        ('5280', '5201'),  # Geel spar met geel licht
        ('5281', '5201'),  # Geel spar met geel licht
        ('5282', '5201'),  # Geel spar met geel licht
        ('5283', '5201'),  # Geel spar met geel licht
        ('5284', '5201'),  # Geel spar met geel licht
        ('5285', '5201'),  # Geel spar met geel licht
        ('5301', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5302', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5303', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5304', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5305', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5306', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5307', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5308', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5309', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5310', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5311', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5312', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5313', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5314', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5315', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5316', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5317', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5318', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5319', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5320', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5321', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5322', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5323', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5324', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5325', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5326', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5327', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5328', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5329', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5330', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5331', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5332', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5333', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5334', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5335', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5351', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5352', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5353', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5354', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5355', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5356', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5357', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5358', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5359', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5360', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5361', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5362', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5363', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5364', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5365', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5366', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5367', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5368', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5369', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5370', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5371', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5372', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5373', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5374', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5375', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5376', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5377', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5378', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5379', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5380', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5381', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5382', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5383', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5384', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5385', '5301'),  # Geel spar met liggend kruis en geel licht
        ('5501', '5501'),  # Geel spits met rood wit rood rechthoek
        ('5502', '5502'),  # Geel spits met rood wit rood rechthoek en geel licht
        ('5511', '5511'),  # Geel stomp met rood wit rood rechthoek
        ('5512', '5512'),  # Geel stomp met rood wit rood rechthoek en geel licht
        ('5521', '5521'),  # Geel bol met rood wit rood rechthoek
        ('5522', '5522'),  # Geel bol met rood wit rood rechthoek en geel licht
        ('5531', '5531'),  # Geel pilaar met rood wit rood rechthoek
        ('5532', '5532'),  # Geel pilaar met rood wit rood rechthoek en geel licht
        ('5541', '5541'),  # Geel spar met rood wit rood rechthoek
        ('5542', '5542'),  # Geel spar met rood wit rood rechthoek en geel licht
        ('6001', '6001'),  # Rood wit bol
        ('6002', '6001'),  # Rood wit bol
        ('6003', '6003'),  # Rood wit bol met rode bol
        ('6004', '6003'),  # Rood wit bol met rode bol
        ('6005', '6005'),  # Rood wit bol met wit licht
        ('6006', '6005'),  # Rood wit bol met wit licht
        ('6007', '6007'),  # Rood wit bol met rode bol en wit licht
        ('6008', '6007'),  # Rood wit bol met rode bol en wit licht
        ('6021', '6021'),  # Rood wit pilaar met rode bol
        ('6022', '6021'),  # Rood wit pilaar met rode bol
        ('6023', '6023'),  # Rood wit pilaar met rode bol en wit licht
        ('6024', '6023'),  # Rood wit pilaar met rode bol en wit licht
        ('6034', '6023'),  # Rood/wit repeterend
        ('6041', '6041'),  # Rood wit spar met rode bol
        ('6042', '6041'),  # Rood wit spar met rode bol
        ('6043', '6043'),  # Rood wit spar met rode bol en wit licht
        ('6044', '6043'),  # Rood wit spar met rode bol en wit licht
        ('7001', '7001'),  # Zwart rood zwart pilaar met 2 zwarte bollen
        ('7002', '7001'),  # Zwart rood zwart pilaar met 2 zwarte bollen
        ('7003', '7003'),  # Zwart rood zwart pilaar met 2 zwarte bollen en wit licht
        ('7004', '7003'),  # Zwart rood zwart pilaar met 2 zwarte bollen en wit licht
        ('7021', '7021'),  # Zwart rood zwart spar met 2 zwarte bollen
        ('7022', '7021'),  # Zwart rood zwart spar met 2 zwarte bollen
        ('7023', '7023'),  # Zwart rood zwart spar met 2 zwarte bollen en wit licht
        ('7024', '7023'),  # Zwart rood zwart spar met 2 zwarte bollen en wit licht
        ('8001', '8001'),  # Blauw geel pilaar
        ('8002', '8002'),  # Blauw geel pilaar met geel staand kruis
        ('9011', '3500'),  # stomp Geel -> missing
        ('Geel', 'Geel'),  # Geel; Geel/zwart; Geel/zwart/geel; Geel/blauw
        ('Geel/zwart', 'Geel'),  # Geel; Geel/zwart; Geel/zwart/geel; Geel/blauw
        ('Geel/zwart/geel', 'Geel'),  # Geel; Geel/zwart; Geel/zwart/geel; Geel/blauw
        ('Geel/Blauw', 'Geel'),  # Geel; Geel/zwart; Geel/zwart/geel; Geel/blauw
        ('Groen', 'Groen'),  # Groen; Groen/rood; Groen/rood/groen; Groen/wit repeterend
        ('Groen/rood', 'Groen'),  # Groen; Groen/rood; Groen/rood/groen; Groen/wit repeterend
        ('Groen/rood/groen', 'Groen'),  # Groen; Groen/rood; Groen/rood/groen; Groen/wit repeterend
        ('Groen/wit repeterend', 'Groen'),  # Groen; Groen/rood; Groen/rood/groen; Groen/wit repeterend
        ('Niet toegewezen', 'Niet toegewezen'),  # Niet toegewezen
        ('Rood', 'Rood'),  # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        ('Rood/groen', 'Rood'),  # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        ('Rood/groen repeterend', 'Rood'),
        ('Rood/groen/rood', 'Rood'),  # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        ('Rood/wit', 'Rood'),  # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        ('Rood/wit repeterend', 'Rood'),  # Rood; Rood/groen; Rood/groen repeterend; Rood/groen/rood; Rood/wit; Rood/wit repeterend
        ('Wit', 'Wit'),  # Wit
        ('Zwart', 'Zwart'),  # Zwart; Zwart/geel; Zwart/geel/zwart; Zwart/rood/zwart
        ('Zwart/geel', 'Zwart'),  # Zwart; Zwart/geel; Zwart/geel/zwart; Zwart/rood/zwart
        ('Zwart/geel/zwart', 'Zwart'),  # Zwart; Zwart/geel; Zwart/geel/zwart; Zwart/rood/zwart
        ('Zwart/rood/zwart', 'Zwart'),  # Zwart; Zwart/geel; Zwart/geel/zwart; Zwart/rood/zwart
        ('NoS57Id', 'NoS57Id'),  # Geen S57 id
        ('10121', '10121'),  # Laterale baken groen topteken
        ('10125', '10121'),  # Laterale baken groen topteken
        ('10131', '10121'),  # Laterale baken groen topteken
        ('10135', '10121'),  # Laterale baken groen topteken
        ('10165', '10121'),  # Laterale baken groen topteken
        ('10122', '10122'),  # Laterale baken groen topteken met groen licht
        ('10126', '10122'),  # Laterale baken groen topteken met groen licht
        ('10132', '10122'),  # Laterale baken groen topteken met groen licht
        ('10136', '10122'),  # Laterale baken groen topteken met groen licht
        ('10166', '10122'),  # Laterale baken groen topteken met groen licht
        ('10111', '10111'),  # Laterale baken rood driehoek topteken
        ('10115', '10111'),  # Laterale baken rood driehoek topteken
        ('10161', '10111'),  # Laterale baken rood driehoek topteken
        ('10112', '10112'),  # Laterale baken rood driehoek topteken met rood licht
        ('10116', '10112'),  # Laterale baken rood driehoek topteken met rood licht
        ('10162', '10112'),  # Laterale baken rood driehoek topteken met rood licht
        ('10171', '10171'),  # Laterale baken splitsing rood en groen topteken
        ('10172', '10172'),  # Laterale baken splitsing rood en groen topteken met wit licht
        ('10156', '10156'),  # Laterale baken groen wit gestreept met groen licht
        ('10155', '10155'),  # Laterale baken groen wit gestreept met groen topteken
        ('10157', '10157'),  # Laterale baken groen wit gestreept met groen topteken met groen licht
        ('10152', '10152'),  # Laterale baken rood wit gestreept met rood licht
        ('10151', '10151'),  # Laterale baken rood wit gestreept met rood topteken
        ('10153', '10153'),  # Laterale baken rood wit gestreept met rood topteken met rood licht
        ('11841', '11841'),  # Bijzondere markering verboden toegang
        ('11843', '11841'),  # Bijzondere markering verboden toegang
        ('11845', '11841'),  # Bijzondere markering verboden toegang
        ('11847', '11841'),  # Bijzondere markering verboden toegang
        ('11842', '11842'),  # Bijzondere markering verboden toegang met geel licht
        ('11844', '11842'),  # Bijzondere markering verboden toegang met geel licht
        ('11846', '11842'),  # Bijzondere markering verboden toegang met geel licht
        ('11848', '11842'),  # Bijzondere markering verboden toegang met geel licht
        ('10272', '10272'),  # Rood groene paal met rode bol en verlichting
        ('10276', '10272'),  # Rood groene paal met rode bol en verlichting
        ('10321', '10321'),  # Geel zwart baken met 2 kegels punten omlaag
        ('10322', '10321'),  # Geel zwart baken met 2 kegels punten omlaag
        ('10323', '10323'),  # Geel zwart baken met 2 kegels punten omlaag en verlichting
        ('10324', '10323'),  # Geel zwart baken met 2 kegels punten omlaag en verlichting
        ('10301', '10301'),  # Zwart geel baken met 2 kegels punten omhoog
        ('10302', '10301'),  # Zwart geel baken met 2 kegels punten omhoog
        ('10303', '10303'),  # Zwart geel baken met 2 kegels punten omhoog en verlichting
        ('10304', '10303'),  # Zwart geel baken met 2 kegels punten omhoog en verlichting
        ('10311', '10311'),  # Zwart geel zwart baken met 2 kegels basis naar elkaar
        ('10312', '10311'),  # Zwart geel zwart baken met 2 kegels basis naar elkaar
        ('10313', '10313'),  # Zwart geel zwart baken met 2 kegels basis naar elkaar en verlichting
        ('10314', '10313'),  # Zwart geel zwart baken met 2 kegels basis naar elkaar en verlichting
        ('10331', '10331'),  # Geel zwart geel baken met 2 kegels punten naar elkaar
        ('10332', '10331'),  # Geel zwart geel baken met 2 kegels punten naar elkaar
        ('10333', '10333'),  # Geel zwart geel baken met 2 kegels punten naar elkaar en verlichting
        ('10334', '10333'),  # Geel zwart geel baken met 2 kegels punten naar elkaar en verlichting
        ('10101', '10101'),  # Rode opstand met cilinder topteken
        ('10105', '10101'),  # Rode opstand met cilinder topteken
        ('10102', '10102'),  # Rode opstand met cilinder topteken en verlichting
        ('10106', '10102'),  # Rode opstand met cilinder topteken en verlichting
        ('11281', '11281'),  # Gele paal met geel liggend kruis
        ('11282', '11281'),  # Gele paal met geel liggend kruis
        ('11283', '11281'),  # Gele paal met geel liggend kruis
        ('11284', '11281'),  # Gele paal met geel liggend kruis
        ('11285', '11281'),  # Gele paal met geel liggend kruis
        ('11286', '11281'),  # Gele paal met geel liggend kruis
        ('11287', '11281'),  # Gele paal met geel liggend kruis
        ('11288', '11281'),  # Gele paal met geel liggend kruis
        ('11289', '11281'),  # Gele paal met geel liggend kruis
        ('11290', '11281'),  # Gele paal met geel liggend kruis
        ('11291', '11281'),  # Gele paal met geel liggend kruis
        ('11292', '11281'),  # Gele paal met geel liggend kruis
        ('11293', '11281'),  # Gele paal met geel liggend kruis
        ('11294', '11281'),  # Gele paal met geel liggend kruis
        ('11295', '11281'),  # Gele paal met geel liggend kruis
        ('11296', '11281'),  # Gele paal met geel liggend kruis
        ('11297', '11281'),  # Gele paal met geel liggend kruis
        ('11298', '11281'),  # Gele paal met geel liggend kruis
        ('11299', '11281'),  # Gele paal met geel liggend kruis
        ('11300', '11281'),  # Gele paal met geel liggend kruis
        ('11301', '11281'),  # Gele paal met geel liggend kruis
        ('11302', '11281'),  # Gele paal met geel liggend kruis
        ('11303', '11281'),  # Gele paal met geel liggend kruis
        ('11304', '11281'),  # Gele paal met geel liggend kruis
        ('11305', '11281'),  # Gele paal met geel liggend kruis
        ('11306', '11281'),  # Gele paal met geel liggend kruis
        ('11307', '11281'),  # Gele paal met geel liggend kruis
        ('11308', '11281'),  # Gele paal met geel liggend kruis
        ('11309', '11281'),  # Gele paal met geel liggend kruis
        ('11310', '11281'),  # Gele paal met geel liggend kruis
        ('11311', '11281'),  # Gele paal met geel liggend kruis
        ('11312', '11281'),  # Gele paal met geel liggend kruis
        ('11313', '11281'),  # Gele paal met geel liggend kruis
        ('11314', '11281'),  # Gele paal met geel liggend kruis
        ('11315', '11281'),  # Gele paal met geel liggend kruis
        ('11321', '11281'),  # Gele paal met geel liggend kruis
        ('11322', '11281'),  # Gele paal met geel liggend kruis
        ('11323', '11281'),  # Gele paal met geel liggend kruis
        ('11324', '11281'),  # Gele paal met geel liggend kruis
        ('11325', '11281'),  # Gele paal met geel liggend kruis
        ('11326', '11281'),  # Gele paal met geel liggend kruis
        ('11327', '11281'),  # Gele paal met geel liggend kruis
        ('11328', '11281'),  # Gele paal met geel liggend kruis
        ('11329', '11281'),  # Gele paal met geel liggend kruis
        ('11330', '11281'),  # Gele paal met geel liggend kruis
        ('11331', '11281'),  # Gele paal met geel liggend kruis
        ('11332', '11281'),  # Gele paal met geel liggend kruis
        ('11333', '11281'),  # Gele paal met geel liggend kruis
        ('11334', '11281'),  # Gele paal met geel liggend kruis
        ('11335', '11281'),  # Gele paal met geel liggend kruis
        ('11336', '11281'),  # Gele paal met geel liggend kruis
        ('11337', '11281'),  # Gele paal met geel liggend kruis
        ('11338', '11281'),  # Gele paal met geel liggend kruis
        ('11339', '11281'),  # Gele paal met geel liggend kruis
        ('11340', '11281'),  # Gele paal met geel liggend kruis
        ('11341', '11281'),  # Gele paal met geel liggend kruis
        ('11342', '11281'),  # Gele paal met geel liggend kruis
        ('11343', '11281'),  # Gele paal met geel liggend kruis
        ('11344', '11281'),  # Gele paal met geel liggend kruis
        ('11345', '11281'),  # Gele paal met geel liggend kruis
        ('11346', '11281'),  # Gele paal met geel liggend kruis
        ('11347', '11281'),  # Gele paal met geel liggend kruis
        ('11348', '11281'),  # Gele paal met geel liggend kruis
        ('11349', '11281'),  # Gele paal met geel liggend kruis
        ('11350', '11281'),  # Gele paal met geel liggend kruis
        ('11351', '11281'),  # Gele paal met geel liggend kruis
        ('11352', '11281'),  # Gele paal met geel liggend kruis
        ('11353', '11281'),  # Gele paal met geel liggend kruis
        ('11354', '11281'),  # Gele paal met geel liggend kruis
        ('11355', '11281'),  # Gele paal met geel liggend kruis
        ('11441', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11442', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11443', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11444', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11445', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11446', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11447', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11448', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11449', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11450', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11451', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11452', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11453', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11454', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11455', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11456', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11457', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11458', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11459', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11460', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11461', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11462', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11463', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11464', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11465', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11466', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11467', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11468', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11469', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11470', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11471', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11472', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11473', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11474', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11475', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11481', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11482', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11483', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11484', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11485', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11486', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11487', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11488', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11489', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11490', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11491', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11492', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11493', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11494', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11495', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11496', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11497', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11498', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11499', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11500', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11501', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11502', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11503', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11504', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11505', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11506', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11507', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11508', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11509', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11510', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11511', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11512', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11513', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11514', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('11515', '11441'),  # Gele paal met geel liggend kruis en verlichting
        ('10261', '10261'),  # Rood groen baken met rode cilinder boven rood bol topteken
        ('10265', '10261'),  # Rood groen baken met rode cilinder boven rood bol topteken
        ('10262', '10262'),  # Rood groen baken met rode cilinder boven rood bol topteken en verlichting
        ('10266', '10262'),  # Rood groen baken met rode cilinder boven rood bol topteken en verlichting
        ('10251', '10251'),  # Groen rood baken met groen kegel boven groen bol topteken
        ('10255', '10251'),  # Groen rood baken met groen kegel boven groen bol topteken
        ('10252', '10252'),  # Groen rood baken met groen kegel boven groen bol topteken en verlichting
        ('10256', '10252'),  # Groen rood baken met groen kegel boven groen bol topteken en verlichting
    ])
)

friesland = BoeienSource(
    name='Friesland',
    source_filename=workingFolder + 'Friesland-Boeien.gml',
    outputFileName='Friesland-Boeien.gpx',
    url=['https://geoportaal.fryslan.nl/arcgis/services/ProvinciaalGeoRegister/PGR2/MapServer/wfsServer?request=GetFeature&service=WFS&version=1.1.0&outputFormat=GML3&typeName=Vaarwegmarkeringen'],

    # mapping Vaarwegmarkeringen feature naam naar GPX field
    field_mapping=dict([('NAAM', {'dst': 'name', 'isDescription': False}),
                        ('TYPE_OMSCHRIJVING', {'dst': 'sym', 'isDescription': True}),
                        ('REGLEMENT_VAARWEGNAAM', {'dst': 'vaarweg', 'isDescription': True}),
                        ('OPMERKING', {'dst': 'opmerking', 'isDescription': True}),
                        ('MODEL', {'dst': 'model', 'isDescription': True}),
                        ('MEER', {'dst': 'meer', 'isDescription': True})
                        ]),

    # Mapping van boei type naar icon S57
    icon_mapping=dict([
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
    ]),
    epsg=28992
)
