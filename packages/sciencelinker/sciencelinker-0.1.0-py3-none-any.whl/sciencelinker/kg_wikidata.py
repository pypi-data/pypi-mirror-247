

from . import kg_generic

WIKIDATA_ENDPOINT = 'https://query.wikidata.org/sparql'

wikidata_type_frequency_query_template = '''
SELECT DISTINCT ?type ?p (COUNT( ?p ) AS ?cnt) WHERE
{ 
    ?s wdt:P31 ?type .
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

wikidata_other_properties_query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?additional_property (COUNT(DISTINCT ?match_value) AS ?cnt) WHERE
{ 
    ?s wdt:P31 <$(TYPE)> .
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

wikidata_enrich_query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?match_value ?target_value WHERE
{ 
    ?s wdt:P31 <$(TYPE)> .
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


def lookup_types(l_values: list, language: str = None) -> list:
    """Find RDF types in Wikidata that are compatible with the given values.

    This is the 1st of 3 steps of the lookup procedure.
    Insert a column or row of your dataset to find RDF types that have these values frequently in their properties.

    :param l_values: A list of values from your dataset
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :return: A list of candidate types with match-making properties and occurrences.
    :rtype: a list of triples like [[type:str,property:str,occurrence:int],...]
    """
    return kg_generic.lookup_types(WIKIDATA_ENDPOINT, l_values, language=language,
                                   query_template=wikidata_type_frequency_query_template)


def lookup_properties(target_type, match_making_property, l_values, language=None) -> list:
    """For a pair of RDF type and match property suggest additional properties that contain data for potential enrichment.

    This is the 2nd of 3 steps of the lookup procedure.
    Select the input from a triple of the output of ``wikidata_lookup_types(...)``.

    :param target_type: The RDF type to look for
    :type target_type: str
    :param match_making_property: The property to use for matching values against
    :type match_making_property: str
    :param l_values: A list of values from your dataset, the same used in step 1.
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :return: A list of candidate properties
    :rtype: list of str
    """
    return kg_generic.lookup_properties(WIKIDATA_ENDPOINT, target_type, match_making_property, l_values,
                                        language=language, query_template=wikidata_other_properties_query_template)


def enrich(target_type: str, match_making_property: str, requested_property: str, l_values: list,
           missing_value: str = 'missing',
           language: str = None, log_name: str = 'default') -> (list, dict):
    """Retrieve additional data from the Wikidata knowledge graph and align it with your input.

    This is the 3rd of 3 steps of the lookup procedure.
    Select the input from the outputs of ``wikidata_lookup_types(...)`` and ``wikidata_lookup_properties(...)``.
    This method will create a dictionary with (value,additional value) pairs and also a list that aligns with l_values to be added to your dataset.

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
    :param log_name: The name of the log to log to
    :type log_name: str, optional
    :return: A list of values aligned with l_values and a dictionary containing pairs of value and additional value
    :rtype: (list, dict)
    """
    return kg_generic.enrich(WIKIDATA_ENDPOINT, target_type, match_making_property, requested_property,
                             l_values, missing_value, language=language, query_template=wikidata_enrich_query_template,
                             log_name=log_name)
