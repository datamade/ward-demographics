import csv
import json
import sys

import scrapelib
from scrapelib.cache import FileCache
from census_area import Census

s = scrapelib.Scraper(raise_errors=False, requests_per_minute=0)
cache = FileCache('cache')

s.cache_storage = cache
s.cache_write_only = False

API_KEY = 'ac94ba69718a7e1da4f89c6d218b8f6b5ae9ac49'

wards = json.load(sys.stdin)
c = Census(API_KEY, session=s)

VARS = {'B03002_001E': 0, # total population,
        'B03002_003E': 0, # Not Hispanic or Latino white
        'B03002_004E': 0, # Not Hispanic or Latino black
        'B03002_006E': 0, # Not Hispanic or Latino asian
        'B03002_012E': 0, # Hispanic or Latino
        'B25120_001E': 0, # Aggregate household income in the past 12 months
        'B19001_001E': 0, # Households
        }

TRACT_LEVEL_VARS = {'B19001_001E', 'B25120_001E'}

READABLE_VARS = {'ward number': None,
                 'B03002_001E': 'Total Population',
                 'B03002_003E': 'Not Hispanic or Latino Origin, Whites',
                 'B03002_004E': 'Not Hispanic or Latino Origin, Blacks',
                 'B03002_006E': 'Not Hispanic or Latino Origin, Asians',
                 'B03002_012E': 'Hispanic or Latino Origin',
                 'B25120_001E': 'Aggregate household income in the past 12 months',
                 'B19001_001E': 'Total households',
                 'mean household income': None,
                 'number of tracts': None,
                 'number of blockgroups': None}

writer = csv.DictWriter(sys.stdout, fieldnames=READABLE_VARS)

writer.writerow({k: (v + '; ' + k) if v else k for k, v in READABLE_VARS.items()})

for ward in wards['features']:
    ward_data = VARS.copy()
    ward_geo = ward['geometry']

    blockgroups = c.acs5.geo_blockgroup(('NAME',) + tuple(VARS), ward_geo)
    total_blockgroups = 0
    for geojson, data, weight in blockgroups:
        for var in (VARS.keys() - TRACT_LEVEL_VARS):
            ward_data[var] += (data[var] * weight)
        total_blockgroups += weight

    tracts = c.acs5.geo_tract(('NAME',) + tuple(VARS), ward_geo)
    total_tracts = 0
    for geojson, data, weight in tracts:
        if data['B25120_001E'] is None:
            data['B25120_001E'] = 0
            data['B19001_001E'] = 0           
        for var in TRACT_LEVEL_VARS:
            ward_data[var] += (data[var] * weight)
        total_tracts += weight 

    ward_data['mean household income'] = ward_data['B25120_001E'] / ward_data['B19001_001E']
    ward_data = {k: int(v) for k, v in ward_data.items()}
    ward_data['ward number'] = ward['properties']['ward']
    ward_data['number of tracts'] = total_tracts
    ward_data['number of blockgroups'] = total_blockgroups

    writer.writerow(ward_data)
