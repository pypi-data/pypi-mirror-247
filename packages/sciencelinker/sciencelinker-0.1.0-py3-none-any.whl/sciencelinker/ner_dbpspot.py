import requests
import urllib.parse
import json
from . import request_cache
from . import processing_log as log

SPOTLIGHT_ENDPOINT = 'https://api.dbpedia-spotlight.org'

# For caching requests
cache = request_cache.RequestCache()


def ner_spotlight_text(l_text: list, language: str, log_name='default') -> list:
    """
    Retrieves entities from a list of given texts using DBpedia Spotlight.

    :param l_text: List of text to find entity mentions in.
    :type l_text: list of str
    :param language: The language of the texts, use 2-letter ISO codes.
    :type language: str
    :param log_name: The name of the log to log to. Default is 'default'
    :type log_name: str
    :return: For each input text a list of entity URLs are returned
    :rtype: list of list of str
    """
    in1 = log.DataItem('l_text', l_text, 'A list of texts as input')
    in2 = log.DataItem('language', language, 'The language to use')
    log.start_procedure('Named entity recognition using DBpedia Spotlight', l_inputs=[in1, in2],
                        method_url='http://sciencelinker.git.gesis.org/docs/lda_gensim.html', log_name=log_name)
    log.add_note(f'Used endpoint: {SPOTLIGHT_ENDPOINT}')

    l_annotations = []
    r = None

    for text in l_text:
        d_query_profile = {'endpoint': SPOTLIGHT_ENDPOINT, 'query': str(l_text)}
        cache_file = cache.get_entry(d_query_profile)
        if cache_file is None:
            params = urllib.parse.urlencode({'text': text})
            url = SPOTLIGHT_ENDPOINT + '/' + language + '/annotate'
            r = requests.get(url, params=params, headers={'Accept': 'application/json'})
            r.encoding = 'utf-8'
            if r.status_code == 200:
                d_results = json.loads(r.text)
                cache_file = cache.create_empty_entry(d_query_profile)
                with open(cache_file, 'w') as fp:
                    json.dump(d_results, fp)
            else:
                raise ('Spotlight returned status: ' + str(r.status_code) + '\n' + r.text)
        else:
            with open(cache_file, 'r') as fp:
                d_results = json.load(fp)
        l_uris = []
        if 'Resources' in d_results:
            for resource in d_results['Resources']:
                l_uris.append(resource['@URI'])
        l_annotations.append(l_uris)

    out1 = log.DataItem('l_annotations', l_annotations, 'List of lists of entity URIs')
    log.end_procedure([out1], log_name=log_name)
    return l_annotations

# def ner_spotlight_url(l_url: list, language: str, log_name='default') -> list:
#     """
#     Retrieves entities from a given web document using DBpedia Spotlight.
#
#     :param l_url: List of URLs to web documents to find entity mentions in.
#     :type l_url: list of str
#     :param language: The language of the texts, use 2-letter ISO codes.
#     :type language: str
#     :param log_name: Name of the log to log to. Default is 'default'
#     :type log_name: str
#     :return: For each input text a list of entity URLs are returned
#     :rtype: list of list of str
#     """
#
#     in1 = log.DataItem('l_url', l_url, 'A list of URLs as input')
#     in2 = log.DataItem('language', language, 'The language to use')
#     log.start_procedure('Named entity recognition using DBpedia Spotlight', l_inputs=[in1, in2])
#     log.add_note(f'Used endpoint: {SPOTLIGHT_ENDPOINT}')
#
#     l_annotations = []
#     r = None
#
#     for query_url in l_url:
#         params = urllib.parse.urlencode({'text': 'No text', 'url': query_url})
#         endpoint_url = SPOTLIGHT_ENDPOINT + '/' + language + '/annotate'
#         r = requests.get(endpoint_url, params=params, headers={'Accept': 'application/json'})
#         r.encoding = 'utf-8'
#
#         if r.status_code == 200:
#             d_results = json.loads(r.text)
#             l_uris = []
#             if 'Resources' in d_results:
#                 for resource in d_results['Resources']:
#                     l_uris.append(resource['@URI'])
#             l_annotations.append(l_uris)
#         else:
#             raise Exception('Spotlight returned status: ' + str(r.status_code)+'\n'+r.text)
#     out1 = log.DataItem('l_annotations', l_annotations, 'List of lists of entity URIs')
#     log.end_procedure([out1], log_name=log_name)
#     return l_annotations
