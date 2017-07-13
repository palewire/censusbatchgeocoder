#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import csv
import logging
import requests
logger = logging.getLogger(__name__)


class Geocoder(object):
    URL = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'
    RESULT_HEADER = [
        'id',
        'input_address',
        'is_match',
        'is_exact',
        'geocoded_address',
        'coordinates',
        'tiger_line',
        'side',
        'state_fips',
        'county_fips',
        'tract',
        'block'
    ]

    def __init__(
        self,
        benchmark='Public_AR_Current',
        vintage='Current_Current',
        return_type='locations',
    ):
        self.benchmark = benchmark
        self.vintage = vintage
        self.return_type = return_type

    def get_payload(self):
        return {
            'benchmark': self.benchmark,
            'vintage': self.vintage,
            'returntype': self.return_type
        }

    def get_response(self, string_or_stream, file_type='text/csv'):
        if hasattr(string_or_stream, 'read'):
            address_file = string_or_stream
        else:
            address_file = open(string_or_stream, 'rb')
        files = {
            'addressFile': ('batch.csv', address_file, file_type)
        }
        logger.debug("Geocoding batch")
        return requests.post(self.URL, files=files, data=self.get_payload())

    def geocode(self, string_or_stream, file_type='text/csv'):
        response = self.get_response(string_or_stream, file_type=file_type)
        data = ",".join(self.RESULT_HEADER) + "\n" + response.text
        return list(csv.DictReader(io.StringIO(data)))


def geocode(
    string_or_stream,
    benchmark='Public_AR_Current',
    vintage='Current_Current',
    return_type='locations',
):
    obj = Geocoder(benchmark=benchmark, vintage=vintage, return_type=return_type)
    return obj.geocode(string_or_stream)
