# python-censusbatchgeocoder

A simple Python wrapper for `U.S. Census Geocoding Services API batch service <https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf>`_.

[![Build Status](https://travis-ci.org/datadesk/python-censusbatchgeocoder.png?branch=master)](https://travis-ci.org/datadesk/python-censusbatchgeocoder)
[![PyPI version](https://badge.fury.io/py/censusbatchgeocoder.png)](http://badge.fury.io/py/censusbatchgeocoder)
[![Coverage Status](https://coveralls.io/repos/datadesk/python-censusbatchgeocoder/badge.png?branch=master)](https://coveralls.io/r/datadesk/python-censusbatchgeocoder?branch=master)

* Issues: [github.com/datadesk/python-censusbatchgeocoder/issues](https://github.com/datadesk/python-censusbatchgeocoder/issues)
* Packaging: [pypi.python.org/pypi/censusbatchgeocoder](https://pypi.python.org/pypi/censusbatchgeocoder)
* Testing: [travis-ci.org/datadesk/python-censusbatchgeocoder](https://travis-ci.org/datadesk/python-censusbatchgeocoder)
* Coverage: [coveralls.io/r/datadesk/python-censusbatchgeocoder](https://coveralls.io/r/datadesk/python-censusbatchgeocoder)

### Installation

```python
pip install censusbatchgeocoder
```

## Basic usage

Importing the library

```python
import censusbatchgeocoder
```

Geocoding a comma-delimited file from the filesystem. Results are returned as a StringIO object.

```python
result = censusbatchgeocoder.geocode("./address.csv")
```

Geocoding an in-memory file object.

```python
data_obj = io.BytesIO(my_data)
result = censusbatchgeocoder.geocode(data_obj)
```
