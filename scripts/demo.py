import csv
import json
import sys

from census_area import Census

API_KEY = 'ac94ba69718a7e1da4f89c6d218b8f6b5ae9ac49'

wards = json.load(sys.stdin)
c = Census(API_KEY)

VARS = {'B03002_001E': 0, # total population,
        'B03002_003E': 0, # Not Hispanic or Latino white
        'B03002_004E': 0, # Not Hispanic or Latino black
        'B03002_006E': 0, # Not Hispanic or Latino asian
        'B03002_012E': 0, # Hispanic or Latino
        'B25120_001E': 0, # Aggregate household income in the past 12 months
        'B19001_001E': 0, # Households
        }

header = ('ward number',) + tuple(VARS) + ('average household income',)
writer = csv.DictWriter(sys.stdout, fieldnames=header)
writer.writeheader()

for ward in wards['features']:
    ward_data = VARS.copy()
    ward_geo = ward['geometry']
    tracts = c.acs5.geo_tract(('NAME',) + tuple(VARS), ward_geo)
    for geojson, data, weight in tracts:
        for var in ward_data:
            ward_data[var] += data[var] * weight
        print(data, file=sys.stderr)

    ward_data['ward number'] = ward['properties']['ward']
    ward_data['average household income'] = ward_data['B25120_001E'] / ward_data['B19001_001E']
    writer.writerow(ward_data)
