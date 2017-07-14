# python-censusbatchgeocoder

A simple Python wrapper for [U.S. Census Geocoding Services API batch service](https://www.documentcloud.org/documents/3894452-Census-Geocoding-Services-API.html).

[![Build Status](https://travis-ci.org/datadesk/python-censusbatchgeocoder.png?branch=master)](https://travis-ci.org/datadesk/python-censusbatchgeocoder)
[![PyPI version](https://badge.fury.io/py/censusbatchgeocoder.png)](http://badge.fury.io/py/censusbatchgeocoder)
[![Coverage Status](https://coveralls.io/repos/datadesk/python-censusbatchgeocoder/badge.png?branch=master)](https://coveralls.io/r/datadesk/python-censusbatchgeocoder?branch=master)

* Issues: [github.com/datadesk/python-censusbatchgeocoder/issues](https://github.com/datadesk/python-censusbatchgeocoder/issues)
* Packaging: [pypi.python.org/pypi/censusbatchgeocoder](https://pypi.python.org/pypi/censusbatchgeocoder)
* Testing: [travis-ci.org/datadesk/python-censusbatchgeocoder](https://travis-ci.org/datadesk/python-censusbatchgeocoder)
* Coverage: [coveralls.io/r/datadesk/python-censusbatchgeocoder](https://coveralls.io/r/datadesk/python-censusbatchgeocoder)

### Installation

```bash
$ pip install censusbatchgeocoder
```

## Basic usage

Importing the library

```python
>>> import censusbatchgeocoder
```

According to the [official Census documentation](https://www.documentcloud.org/documents/3894452-Census-Geocoding-Services-API.html), the input file is expected to contain a comma-delimited list of addresses segmented into the following fields:

* ``id``: Your unique identifier for the record
* ``address``: Structure number and street name (required)
* ``city``: City name (required)
* ``state``: State (optional)
* ``zipcode``: ZIP Code (optional)

An example could look like this:

```text
id,address,city,state,zipcode
1,1600 Pennsylvania Ave NW,Washington,DC,20006
2,202 W. 1st Street,Los Angeles,CA,90012
```

Geocoding a comma-delimited file from the filesystem. Results are returned as a list of dictionaries.

```python
>>> censusbatchgeocoder.geocode("./my_file.csv")
[{'input_address': '202 W. 1st Street, Los Angeles, CA, 90012',
  'block': '1034',
  'coordinates': '-118.24456,34.053005',
  'county_fips': '037',
  'geocoded_address': '202 W 1ST ST, LOS ANGELES, CA, 90012',
  'id': '2',
  'is_exact': 'Exact',
  'is_match': 'Match',
  'side': 'L',
  'state_fips': '06',
  'tiger_line': '141618115',
  'tract': '207400'},
 {'input_address': '1600 Pennsylvania Ave NW, Washington, DC, 20006',
  'block': '1031',
  'coordinates': '-77.03535,38.898754',
  'county_fips': '001',
  'geocoded_address': '1600 PENNSYLVANIA AVE NW, WASHINGTON, DC, 20502',
  'id': '1',
  'is_exact': 'Non_Exact',
  'is_match': 'Match',
  'side': 'L',
  'state_fips': '11',
  'tiger_line': '76225813',
  'tract': '006202'}]
```

You can also geocode an in-memory file object.

```python
>>> my_data = """id,address,city,state,zipcode
1,1600 Pennsylvania Ave NW,Washington,DC,20006
2,202 W. 1st Street,Los Angeles,CA,90012"""
>>> censusbatchgeocoder.geocode(io.StringIO(my_data))
[{'address': '202 W. 1st Street, Los Angeles, CA, 90012',
  'block': '1034',
  'coordinates': '-118.24456,34.053005',
  'county_fips': '037',
  'geocoded_address': '202 W 1ST ST, LOS ANGELES, CA, 90012',
  'id': '2',
  'is_exact': 'Exact',
  'is_match': 'Match',
  'side': 'L',
  'state_fips': '06',
  'tiger_line': '141618115',
  'tract': '207400'},
 {'address': '1600 Pennsylvania Ave NW, Washington, DC, 20006',
  'block': '1031',
  'coordinates': '-77.03535,38.898754',
  'county_fips': '001',
  'geocoded_address': '1600 PENNSYLVANIA AVE NW, WASHINGTON, DC, 20502',
  'id': '1',
  'is_exact': 'Non_Exact',
  'is_match': 'Match',
  'side': 'L',
  'state_fips': '11',
  'tiger_line': '76225813',
  'tract': '006202'}]
```
