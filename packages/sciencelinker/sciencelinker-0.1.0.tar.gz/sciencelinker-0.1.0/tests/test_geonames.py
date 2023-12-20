#!/bin/python3
from sciencelinker import geo_names
from sciencelinker import processing_log as log

l_query_terms = ['London', 'Paris', 'Berlin', 'Madrid', 'Antananarivo']
l_allowed_countries = ['GB', 'FR', 'DE', 'ES', 'MG']
min_population = 5000

l_long, l_lat = geo_names.get_long_lat(l_query_terms, l_allowed_countries, geo_names.REGION_TYPE_COUNTRY_STATE_REGION,
                                       min_population)

for i in range(len(l_query_terms)):
    print(l_query_terms[i] + '\t\t' + l_long[i] + '\t\t' + l_lat[i])

if len(l_long) == 5 and len(l_lat) == 5:
    print('Test OK')
else:
    print('Test failed')

# s = log.write_log(output_format='json')
# print(s)
