"""Chart
Part of the ChartCatalogs project
Copyright (c) 2015 Pavel Kalian : Original implementation
Copyright (c) 2022 Marcel Verpaalen : Minor updates
Licensed under GPLv2 or, at yoir will later version
"""

from xml.etree.ElementTree import Element, SubElement, tostring


class Chart:
    def __init__(self):
        self.number = 0
        self.title = ''
        self.url = ''
        self.ntm_edition_last_correction = None
        self.vertical_datum = None
        self.horizontal_datum = None
        self.chart_format = None
        self.zipfile_ts = None
        self.zipfile_size = 0
        self.target_filename = None

    def is_valid(self):
        return self.number != 0 and self.title != '' and self.url != '' and self.zipfile_ts != None

    def append_xml_element(self, parent, chart_name_include_number=False):
        e = SubElement(parent, 'chart')
        e.tail = '\n'
        child = SubElement(e, 'number')
        child.text = self.number
        child = SubElement(e, 'title')
        if chart_name_include_number:
            child.text = self.title + " (" + self.number + ")"
        else:
            child.text = self.title
        if self.vertical_datum != None:
            child = SubElement(e, 'vertical_datum')
            child.text = self.vertical_datum
        if self.horizontal_datum != None:
            child = SubElement(e, 'horizontal_datum')
            child.text = self.horizontal_datum
        if self.chart_format != None:
            child = SubElement(e, 'format')
            child.text = self.chart_format
        child = SubElement(e, 'zipfile_location')
        child.text = self.url
        child = SubElement(e, 'zipfile_datetime')
        child.text = self.zipfile_ts.strftime('%Y%m%d_%H%M%S')
        child = SubElement(e, 'zipfile_datetime_iso8601')
        child.text = self.zipfile_ts.strftime('%Y-%m-%dT%H:%M:%SZ')
        if self.zipfile_size > 0:
            child = SubElement(e, 'zipfile_size')
            child.text = self.zipfile_size
        if self.ntm_edition_last_correction != None:
            child = SubElement(e, 'ntm_edition_last_correction')
            child.text = self.ntm_edition_last_correction
        if self.target_filename != None:
            child = SubElement(e, 'target_filename')
            child.text = self.target_filename

    def print_info(self):
        print(self.number)
        print(self.title)
        print(self.url)
        print(self.ntm_edition_last_correction)
