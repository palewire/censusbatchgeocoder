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
        self.small_path = os.path.join(self.this_dir, 'small.csv')
        self.big_path = os.path.join(self.this_dir, 'big.csv')

    def test_stringio(self):
        with open(self.small_path, 'r') as f:
            sample = io.BytesIO(f.read())
        result = censusbatchgeocoder.geocode(sample)
        self.assertEqual(len(result), 5)

    def test_path(self):
        result = censusbatchgeocoder.geocode(self.small_path)
        self.assertEqual(len(result), 5)

    # def test_big_batch(self):
    #     result = censusbatchgeocoder.geocode(self.big_path)
    #     self.assertEqual(len(result), 1498)
