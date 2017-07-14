#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import csv
import six
import logging
import requests
import multiprocessing
from multiprocessing.pool import ThreadPool
logger = logging.getLogger(__name__)


class Geocoder(object):
    """
    Wrapper on the Census Geocoding Services API batch service.
    """
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
        batch_size=1000,
        pooling=True,
    ):
        self.benchmark = benchmark
        self.vintage = vintage
        self.return_type = return_type
        self.batch_size = batch_size
        self.pooling = pooling

    def get_payload(self):
        """
        Returns the payload to include with the geocoder request.
        """
        return {
            'benchmark': self.benchmark,
            'vintage': self.vintage,
            'returntype': self.return_type
        }

    def get_response(self, address_file):
        """
        Returns the raw geocoder result for the provided address file.
        """
        files = {
            'addressFile': ('batch.csv', address_file, 'text/csv')
        }
        logger.debug("Sending request")
        return requests.post(self.URL, files=files, data=self.get_payload())

    def get_chunks(self, l):
        """
        Breaks up the provided list into chunks.
        """
        # For item i in a range that is a length of l,
        for i in range(0, len(l), self.batch_size):
            # Create an index range for l of n items:
            yield l[i:i+self.batch_size]

    def _handle_chunk(self, chunk):
        """
        Geocodes the provided chunk and appends it to the response file.
        """
        if six.PY3:
            io_klass = io.StringIO
        else:
            io_klass = io.BytesIO

        # Convert the chunk into a file object again
        chunk_file = io_klass()
        chunk_writer = csv.writer(chunk_file)
        chunk_writer.writerows(chunk)

        # Request batch from the API
        request_file = io_klass(chunk_file.getvalue())
        response = self.get_response(request_file)

        # Add the response to what we return
        self.response_file.write(response.text)

    def geocode(self, string_or_stream):
        """
        Accepts a file object or path with a batch of addresses and attempts to geocode it.
        """
        # Depending on what kind of data has been submitted prepare the file object
        if hasattr(string_or_stream, 'read'):
            address_file = string_or_stream
        else:
            address_file = open(string_or_stream, 'r')

        # Read it in as a csv
        address_csv = list(csv.reader(address_file))

        # Break it into chunks
        address_chunks = list(self.get_chunks(address_csv))

        # Create the string we'll build on the fly as we hit the API and process responses
        self.response_file = io.StringIO()

        # Toss in the header
        self.response_file.write(",".join(self.RESULT_HEADER) + "\n")

        # Loop through the chunks and get results for them one at a time
        if self.pooling:
            cpu_count = multiprocessing.cpu_count()
            logger.debug("Pooling on {} CPUs".format(cpu_count))
            pool = ThreadPool(processes=cpu_count)
            pool.map(self._handle_chunk, address_chunks)
        else:
            [self._handle_chunk(c) for c in address_chunks]

        # Parse the response file as a CSV
        csv_file = io.StringIO(self.response_file.getvalue())
        response_list = csv.DictReader(csv_file)

        # Pass it back
        return list(response_list)


def geocode(
    string_or_stream,
    benchmark='Public_AR_Current',
    vintage='Current_Current',
    return_type='locations',
    batch_size=1000,
    pooling=True,
):
    """
    Accepts a file object or path with a batch of addresses and attempts to geocode it.
    """
    obj = Geocoder(
        benchmark=benchmark,
        vintage=vintage,
        return_type=return_type,
        batch_size=batch_size,
        pooling=pooling
    )
    return obj.geocode(string_or_stream)
