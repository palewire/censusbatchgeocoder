#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests censusbatchgeocoder wrapper.
"""
from __future__ import unicode_literals
import io
import os
import six
import unittest
import censusbatchgeocoder


class GeocoderTest(unittest.TestCase):

    def setUp(self):
        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.small_path = os.path.join(self.this_dir, 'small.csv')
        self.incomplete_path = os.path.join(self.this_dir, 'incomplete.csv')
        self.weird_path = os.path.join(self.this_dir, 'weird.csv')
        self.extra_path = os.path.join(self.this_dir, 'extra.csv')
        self.big_path = os.path.join(self.this_dir, 'big.csv')

    def test_stringio(self):
        with open(self.small_path, 'r') as f:
            if six.PY3:
                sample = io.StringIO(f.read())
            else:
                sample = io.BytesIO(f.read())
        result = censusbatchgeocoder.geocode(sample)
        self.assertEqual(len(result), 5)

    def test_path(self):
        result = censusbatchgeocoder.geocode(self.small_path)
        self.assertEqual(len(result), 5)

    def test_extra_columns(self):
        result = censusbatchgeocoder.geocode(self.extra_path)
        self.assertEqual(len(result), 5)

    def test_weird_headers(self):
        result = censusbatchgeocoder.geocode(
            self.weird_path,
            id="foo",
            address="bar",
            city="baz",
            state="bada",
            zipcode="boom"
        )
        self.assertEqual(len(result), 5)

    def test_no_state_and_zipcode(self):
        result = censusbatchgeocoder.geocode(self.incomplete_path, state=None, zipcode=None)
        self.assertEqual(len(result), 5)

    def test_nopooling(self):
        result = censusbatchgeocoder.geocode(self.small_path, pooling=False)
        self.assertEqual(len(result), 5)

    def test_batch_size(self):
        result = censusbatchgeocoder.geocode(self.small_path, batch_size=2)
        self.assertEqual(len(result), 5)

    # def test_big_batch(self):
    #     result = censusbatchgeocoder.geocode(self.big_path)
    #     self.assertEqual(len(result), 1498)
