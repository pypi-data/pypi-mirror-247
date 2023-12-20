"""The sciencelinker.kg_generic module compiles a wide range of functionalities specifically designed for efficiently retrieving
information from conventional RDF triple stores using SPARQL queries.

This module operates through three distinct steps, each serving a crucial purpose in the data enrichment process:

1. ``lookup_types(...)``: In this initial step, suitable RDF types and match-making properties are retrieved. These serve as the basis for identifying relevant resources within the triple store.
2. ``lookup_properties(...)``: Following the selection of a type and match-making property from step 1, this step enables the retrieval of a comprehensive list of properties. These properties serve as sources of additional data that can be drawn upon to enrich the existing dataset.
3. ``enrich(...)``: The final step involves the actual enrichment process. By combining the selected type, match-making property, and additional-data property obtained from steps 1 and 2, this function performs the necessary operations to augment the dataset with the retrieved additional data.

Caching: ScienceLinker uses a caching mechanism for calls to web services and endpoints. When a query is repeated within 24h the result is used from a cache.
This is necessary to reduce the load on external resources and also has performance advantages during testing. If you have to retrieve recent data you can
delete the cached data, it is stored at ``.request_cache``.

"""

import json
import SPARQLWrapper
from . import request_cache
from . import processing_log as log

type_frequency_query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?type ?p (COUNT( ?p ) AS ?cnt) WHERE
{ 
    ?s a ?type .
    ?s ?p ?match_value .
    FILTER(isLiteral(?match_value))
    VALUES(?match_value)
    {
$(VALUES)
    }
}
GROUP BY ?type ?p
ORDER BY DESC(?cnt)
'''

other_properties_query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?additional_property (COUNT(DISTINCT ?match_value) AS ?cnt) WHERE
{ 
    ?s a <$(TYPE)> .
    ?s <$(MATCH_PROPERTY)> ?match_value .
    ?s ?additional_property ?some_value .
    FILTER (isLiteral(?match_value))
    FILTER (isLiteral(?some_value)) 
    VALUES(?match_value)
    {
        $(VALUES)
    }
}
GROUP BY ?additional_property
ORDER BY DESC(?cnt)
'''

enrich_query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?match_value ?target_value WHERE
{ 
    ?s a <$(TYPE)> .
    ?s <$(MATCH_PROPERTY)> ?match_value .
    ?s <$(ADDITIONAL_PROPERTY)> ?target_value .
    FILTER (isLiteral(?match_value))
    FILTER (isLiteral(?target_value))
    VALUES(?match_value)
    {
        $(VALUES)
    }
}
'''

# For caching requests
cache = request_cache.RequestCache()


def execute_query(endpoint, query):
    sparql = SPARQLWrapper.SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    sparql.setMethod('POSTDIRECTLY')

    d_query_profile = {'endpoint': endpoint, 'query': str(query)}
    cache_file = cache.get_entry(d_query_profile)
    if cache_file is None:
        results = sparql.query().convert()
        cache_file = cache.create_empty_entry(d_query_profile)
        with open(cache_file, 'w') as fp:
            json.dump(results, fp)
    else:
        with open(cache_file, 'r') as fp:
            results = json.load(fp)
    return results


def lookup_types(endpoint: str, l_values: list, language: str = None, query_template=None) -> list:
    """Find RDF types in a triplestore that are compatible with the given values.

    This is the 1st of 3 steps of the lookup procedure.
    Insert a column or row of your dataset to find RDF types that have these values frequently in their properties.

    :param endpoint: URL of the triplestore's SPARQL interface
    :type endpoint: URL as str
    :param l_values: A list of values from your dataset
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :param query_template: SPARQL query template to use. If none is given ``sciencelinker.lookup.type_frequency_query_template`` will be used.
    :type query_template: str, optional
    :return: A list of candidate types with match-making properties and occurrences.
    :rtype: A list of lists like [[type:str,property:str,occurrence:int],...]
    """

    values_str = ''
    indent = '        '
    language_tag = ''
    if language is not None:
        language_tag = '@' + language
    for value in sorted(set(l_values)):
        values_str += indent + '("' + str(value) + '"' + language_tag + ')\n'
    if query_template is None:
        query = type_frequency_query_template
    else:
        query = query_template
    query = query.replace('$(VALUES)', values_str)
    print(query)

    results = execute_query(endpoint, query)
    l_candidate_types = []
    if len(results) == 0:
        return []
    else:
        for row in results["results"]["bindings"]:
            l_candidate_types.append([str(row['type']['value']), str(row['p']['value']), int(row['cnt']['value'])])

    frequency_index = 2
    l_candidate_types.sort(key=lambda x: x[frequency_index], reverse=True)
    return l_candidate_types


def lookup_properties(endpoint: str, target_type: str, match_making_property: str, l_values: list, language: str = None,
                      query_template=None) -> list:
    """For a pair of RDF type and match property suggest additional properties that contain data for potential enrichment.

    This is the 2nd of 3 steps of the lookup procedure.
    Select the input from a triple of the output of ``lookup_types(...)``.

    :param endpoint: URL of the triplestore's SPARQL interface
    :type endpoint: URL as str
    :param target_type: The RDF type to look for
    :type target_type: str
    :param match_making_property: The property to use for matching values against
    :type match_making_property: str
    :param l_values: A list of values from your dataset, the same used in step 1.
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :param query_template: SPARQL query template to use. If none is given ``sciencelinker.lookup.other_properties_query_template`` will be used.
    :type query_template: str, optional
    :return: A list of candidate properties
    :rtype: list of str
    """
    indent = '        '
    language_tag = ''
    if language is not None:
        language_tag = '@' + language
    values_str = ''
    for value in sorted(set(l_values)):
        values_str += indent + '("' + str(value) + '"' + language_tag + ')\n'

    if query_template is None:
        query = other_properties_query_template
    else:
        query = query_template

    query = query.replace('$(TYPE)', target_type)
    query = query.replace('$(MATCH_PROPERTY)', match_making_property)
    query = query.replace('$(VALUES)', values_str)
    print(query)
    results = execute_query(endpoint, query)
    l_candidate_preds = []
    if len(results) == 0:
        return []
    else:
        for row in results["results"]["bindings"]:
            l_candidate_preds.append([str(row['additional_property']['value']), int(row['cnt']['value'])])
    return l_candidate_preds


def enrich(endpoint: str, target_type: str, match_making_property: str, requested_property: str, l_values: list,
           missing_value: str, language: str = None, query_template=None, log_name='default') -> (list, dict):
    """Retrieve additional data from the knowledge graph and align it with your input.

    This is the 3rd of 3 steps of the lookup procedure.
    Select the input from the outputs of ``lookup_types(...)`` and `lookup_properties(...)``.
    This method will create a dictionary with (value,additional value) pairs and also a list that aligns with l_values to be added to your dataset.

    :param endpoint: URL of the triplestore's SPARQL interface
    :type endpoint: URL as str
    :param target_type: The RDF type to look for
    :type target_type: str
    :param match_making_property: The property to use for matching values against
    :type match_making_property: str
    :param requested_property: The property that holds the additional values
    :type requested_property: str
    :param l_values: A list of values from your dataset, the same used in step 1.
    :type l_values: list
    :param missing_value: The value to be used in case no match could be performed (default is 'missing')
    :type missing_value: Any, optional
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :param query_template: SPARQL query template to use. If none is given ``sciencelinker.lookup.enrich_query_template`` will be used.
    :type query_template: str, optional
    :return: A list of values aligned with l_values and a dictionary containing pairs of value and additional value
    :rtype: (list, dict)
    """

    # Log info
    in1 = log.DataItem(name="endpoint", value=endpoint, description='SPARQL endpoint of the knowledge base')
    in2 = log.DataItem(name="target_type", value=target_type, description='Rdf:type of candidate resources')
    in3 = log.DataItem(name="match_making_property", value=match_making_property,
                       description='Property in the KB to match against')
    in4 = log.DataItem(name="requested_property", value=requested_property,
                       description='Property containing the additional piece of information for enrichment')
    in5 = log.DataItem(name="l_values", value=l_values, description='Original data / source data')
    in6 = log.DataItem(name="missing_value", value=missing_value,
                       description='The value to enlist if no match could be found')
    in7 = log.DataItem(name="language", value=language, description='The language tag of the data in the KB')
    in8 = log.DataItem(name="query_template", value=query_template,
                       description='The SPARQL query template to use for the KB')
    in9 = log.DataItem(name="log_name", value=log_name, description='The name of the logger to use')
    log.start_procedure(name="Data linking with DBpedia", l_inputs=[in1, in2, in3, in4, in5, in6, in7],
                        method_url='http://sciencelinker.git.gesis.org/docs/kg_generic.html',
                        log_name=log_name)

    indent = '        '
    language_tag = ''
    if language is not None:
        language_tag = '@' + language

    values_str = ''
    for value in sorted(set(l_values)):
        values_str += indent + '("' + str(value) + '"' + language_tag + ')\n'

    if query_template is None:
        query = enrich_query_template
    else:
        query = query_template
    query = query.replace('$(TYPE)', target_type)
    query = query.replace('$(MATCH_PROPERTY)', match_making_property)
    query = query.replace('$(ADDITIONAL_PROPERTY)', requested_property)
    query = query.replace('$(VALUES)', values_str)

    results = execute_query(endpoint, query)
    d = {}
    if len(results) == 0:
        return [], {}
    else:
        for row in results["results"]["bindings"]:
            if str(row['match_value']['value']) not in d:
                d[str(row['match_value']['value'])] = str(row['target_value']['value'])
    l_target_values = []
    for value in l_values:
        if value in d:
            l_target_values.append(d[value])
        else:
            l_target_values.append(missing_value)

    out1 = log.DataItem('l_target_values', l_target_values,
                        'A list of the requested data that aligns with the input data')
    out2 = log.DataItem('d', d, 'A dictionary with pairs of original values and additional values')
    log.end_procedure([out1, out2], log_name)
    return l_target_values, d
