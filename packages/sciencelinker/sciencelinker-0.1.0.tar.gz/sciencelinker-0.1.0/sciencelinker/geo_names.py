import sys

import requests
import urllib.parse
import json
from . import request_cache
from . import processing_log as log

GEONAMES_ENDPOINT = 'https://secure.geonames.org/search'
MAX_ROWS = '500'
RETURN_TYPE = 'json'
USER_NAME = 'sltest'

REGION_TYPE_CITY_VILLAGE = 0
REGION_TYPE_PARK_AREA = 1
REGION_TYPE_COUNTRY_STATE_REGION = 2

# For caching requests
cache = request_cache.RequestCache()


def _retrieve_geodata(l_search_term, language='en'):
    query_terms = urllib.parse.quote(','.join(set(l_search_term)))

    url = GEONAMES_ENDPOINT + '?name=' + query_terms
    url += '&lang=' + language
    url += '&operator=OR'
    url += '&isNameRequired=true'
    url += '&orderby=population'
    url += '&maxRows=' + MAX_ROWS
    url += '&type=' + RETURN_TYPE
    url += '&username=' + USER_NAME

    d_query_profile = {'endpoint': url, 'query': str(query_terms)}
    cache_file = cache.get_entry(d_query_profile)
    if cache_file is None:
        r = requests.get(url)

        if r.status_code == 200:
            cache_file = cache.create_empty_entry(d_query_profile)
            d = json.loads(r.text)
            with open(cache_file, 'w') as fp:
                json.dump(d, fp)
        else:
            print('Status Code:')
            print(r.status_code)
            print(r.text)
            return None
    else:
        with open(cache_file, 'r') as fp:
            d = json.load(fp)
    return d


def _select_geodata(d, l_search_term, l_country_codes, min_population, region_type):
    d_res = {}
    for term in l_search_term:
        d_res[term] = 'missing'
    for entry in d['geonames']:
        if (entry['fclName'] == 'city, village,...' and region_type == REGION_TYPE_CITY_VILLAGE) or (
                entry['fclName'] == 'parks,area, ...' and region_type == REGION_TYPE_PARK_AREA) or (
                entry['fclName'] == 'country, state, region,...' and region_type == REGION_TYPE_COUNTRY_STATE_REGION):
            if entry['countryCode'] in l_country_codes:
                if entry['population'] >= min_population:
                    for key in d_res:
                        if key in entry['name']:  # Find relevant key
                            if d_res[key] == 'missing':  # Existing entry was empty
                                d_res[key] = entry
                            elif d_res[key]['name'] == entry['name']:  # New entry is perfect match
                                d_res[key] = entry
                            else:
                                if len(d_res[key]['name']) > len(entry['name']):
                                    d_res[key] = entry
    return d_res


def _prepare_geodata(l_query_terms, d):
    l_longitude = []
    l_latitude = []
    for t in l_query_terms:
        if d[t] == 'missing':
            l_longitude.append('missing')
            l_latitude.append('missing')
        else:
            l_longitude.append(d[t]['lng'])
            l_latitude.append(d[t]['lat'])
    return l_longitude, l_latitude, d


def get_long_lat(l_search_terms: list, l_country_codes: list, region_type: int, min_population: int, language: str='en',
                 log_name='default') -> (list, list):
    """
    Retrieve longitude-latitude pairs for a list of place names.

    The search can be limited to geographic areas using country codes and predefined region codes,
    also minimum population can be stated to reduce search space.

    :param language: Language of the search terms in `ISO-693-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ 2-letter codes
    :type language: str
    :param l_search_terms: List of place names
    :type l_search_terms: list of str
    :param l_country_codes: List of `ISO-3166 <https://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements>`_ 2-letter country codes to limit the search space e.g. ['GB', 'FR', 'DE', 'SP', 'MG']
    :type l_country_codes: list of str
    :param region_type: A region type to limit the search space
    :type region_type: int, available values are REGION_TYPE_CITY_VILLAGE, REGION_TYPE_PARK_AREA, REGION_TYPE_COUNTRY_STATE_REGION
    :param min_population: A minimum population for places to limit the search space
    :type min_population: int
    :return: A list of longitudes and a list of latitudes both aligning with l_search_terms. The coordinates are in the `WGS84 <https://en.wikipedia.org/wiki/World_Geodetic_System#WGS_84>`_ format.
    :rtype: (list,list)
    """
    in1 = log.DataItem(name='l_search_terms', value=l_search_terms, description='List of location names')
    in2 = log.DataItem(name='l_country_codes', value=l_country_codes, description='Codes of country to consider')
    in3 = log.DataItem(name='region_type', value=region_type, description='Type of region to consider')
    in4 = log.DataItem(name='min_population', value=min_population,
                       description='Minimum population for locations to consider')
    in5 = log.DataItem(name='language', value=language, description='The language of the search terms')
    log.start_procedure(name='Geodata retrieval', l_inputs=[in1, in2, in3, in4, in5],
                        method_url='http://sciencelinker.git.gesis.org/docs/geo_names.html', log_name=log_name)
    log.add_note(f"Geonames endpoint: {GEONAMES_ENDPOINT}", log_name=log_name)
    log.add_note('Missing values = "missing"', log_name=log_name)

    d_geo = _retrieve_geodata(l_search_terms, language=language)
    if 'geonames' not in d_geo:
        raise Exception(f'Error: \n{d_geo}')
    d_selected_data = _select_geodata(d_geo, l_search_terms, l_country_codes, min_population, region_type)
    l_long, l_lat, d = _prepare_geodata(l_search_terms, d_selected_data)

    out1 = log.DataItem(name='l_long', value=l_long, description='List of longitudes')
    out2 = log.DataItem(name='l_lat', value=l_lat, description='List of latitudes')
    log.end_procedure(l_outputs=[out1, out2], log_name=log_name)
    return l_long, l_lat
