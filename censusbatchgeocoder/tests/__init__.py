#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests censusbatchgeocoder wrapper.
"""
from __future__ import unicode_literals
import io
import os
import unittest
import censusbatchgeocoder


class GeocoderTest(unittest.TestCase):

    def setUp(self):
        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.test_path = os.path.join(self.this_dir, 'test.csv')

    def test_stringio(self):
        sample = io.BytesIO(open(self.test_path, 'rb').read())
        censusbatchgeocoder.geocode(sample)

    def test_path(self):
        censusbatchgeocoder.geocode(self.test_path)
