#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import six
import agate
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
        'geocoded_address',
        'is_match',
        'is_exact',
        'returned_address',
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
        id="id",
        address="address",
        city="city",
        state="state",
        zipcode="zipcode",
        encoding=None,
        user_agent="python-censusbatchgeocoder (https://github.com/datadesk/python-censusbatchgeocoder)"
    ):
        self.benchmark = benchmark
        self.vintage = vintage
        self.return_type = return_type
        self.batch_size = batch_size
        self.pooling = pooling
        self.field_names = {
            'id': id,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode
        }
        self.encoding = encoding
        self.agate_options = {}
        if self.encoding and six.PY2:
            self.agate_options['encoding'] = self.encoding
        self.user_agent = user_agent

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
        headers = {
            'User-Agent': self.user_agent
        }
        logger.debug("Sending request")
        return requests.post(self.URL, headers=headers, files=files, data=self.get_payload())

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
        chunk_writer = agate.csv.writer(chunk_file)
        for row_dict in chunk:
            # Start off with the required fields
            row_list = [
                row_dict[self.field_names['id']],
                row_dict[self.field_names['address']],
                row_dict[self.field_names['city']],
            ]

            # Add optional fields, if they are provided
            if self.field_names['state'] is not None:
                row_list.append(row_dict[self.field_names['state']])
            else:
                row_list.append('')
            if self.field_names['zipcode'] is not None:
                row_list.append(row_dict[self.field_names['zipcode']])
            else:
                row_list.append('')

            # Write it out to the file object
            chunk_writer.writerow(row_list)

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
            # This if for file objects
            request_file = string_or_stream
            request_csv = list(agate.csv.DictReader(request_file, **self.agate_options))
        elif isinstance(string_or_stream, six.string_types):
            # This is for strings that should be a path leading to a file
            if six.PY3 and self.encoding:
                request_file = open(string_or_stream, 'r', encoding=self.encoding)
            else:
                request_file = open(string_or_stream, 'r')
            request_csv = list(agate.csv.DictReader(request_file, **self.agate_options))
        else:
            # Otherwise we assume it's a list of dictionaries ready to go
            request_csv = string_or_stream

        # Break it into chunks
        request_chunks = list(self.get_chunks(request_csv))

        # Create the string we'll build on the fly as we hit the API and process responses
        self.response_file = io.StringIO()

        # Toss in the header
        self.response_file.write(
            "{}\n".format(",".join(self.RESULT_HEADER)),
        )

        # Loop through the chunks and get results for them one at a time
        if self.pooling:
            cpu_count = multiprocessing.cpu_count()
            logger.debug("Pooling on {} CPUs".format(cpu_count))
            pool = ThreadPool(processes=cpu_count)
            pool.map(self._handle_chunk, request_chunks)
        else:
            [self._handle_chunk(c) for c in request_chunks]

        # Parse the response file as a CSV
        if six.PY2:
            csv_io_klass = io.BytesIO
            csv_file = csv_io_klass(self.response_file.getvalue().encode("utf-8"))
        else:
            csv_io_klass = io.StringIO
            csv_file = csv_io_klass(self.response_file.getvalue())

        # Read it back in
        response_list = list(agate.csv.DictReader(csv_file))

        # Merge it with the input file by first making a lookup by id
        response_lookup = dict((d['id'], d) for d in response_list)

        # Create a new list to store the combined data
        combined_list = []

        # Loop through all of the rows in the request
        for request_row in request_csv:
            # For each one grab the response data
            row_key = "{}".format(request_row[self.field_names['id']])
            response_row = response_lookup[row_key]

            # Pop the id out of the response since it's already in the request
            del response_row['id']

            # Add the response data to the request row
            request_row.update(response_row)

            # Add it to the combined list
            combined_list.append(request_row)

        # Pass it back
        return combined_list


def geocode(string_or_stream, **kwargs):
    """
    Accepts a file object or path with a batch of addresses and attempts to geocode it.
    """
    obj = Geocoder(**kwargs)
    return obj.geocode(string_or_stream)
