from . import kg_generic

DBPEDIA_ENDPOINT = 'https://dbpedia.org/sparql'


def lookup_types(l_values: list, language: str = None) -> list:
    """Find RDF types and matching properties in DBpedia that are compatible with the list of given values.

    :param l_values: A list of values from your dataset
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :return: A list of candidate types with match-making properties and occurrences.
    :rtype: A list of lists like [[type:str,property:str,occurrence:int],...]
    """
    return kg_generic.lookup_types(DBPEDIA_ENDPOINT, l_values, language=language)


def lookup_properties(target_type: str, match_making_property: str, l_values: list,
                      language: str = None) -> list:
    """For a pair of RDF type and match property suggest additional properties that contain data for potential enrichment.

    Select the input from a triple of the output of ``dbpedia_lookup_types(...)``.

    :param target_type: The RDF type to look for
    :type target_type: str
    :param match_making_property: The property to use for value matching
    :type match_making_property: str
    :param l_values: A list of values from your dataset, the same as used in step 1
    :type l_values: list
    :param language: The language of the values in 2-letter ISO codes (default is None)
    :type language: str, optional
    :return: A list of candidate properties
    :rtype: list of str
    """
    return kg_generic.lookup_properties(DBPEDIA_ENDPOINT, target_type, match_making_property, l_values,
                                        language=language)


def enrich(target_type: str, match_making_property: str, requested_property: str, l_values: list,
           missing_value: str = 'missing',
           language: str = None, log_name: str = 'default') -> (list, dict):
    """Retrieve additional data from the DBpedia KG and align it with your input.

    Select the input from the outputs of ``dbpedia_lookup_types(...)`` and ``dbpedia_lookup_properties(...)``.
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
    :param log_name: The name of the log to log to (default is 'default')
    :type log_name: str, optional
    :return: A list of values aligned with l_values and a dictionary containing pairs of value and corresponding additional value
    :rtype: (list, dict)
    """

    retlist, retdict = kg_generic.enrich(DBPEDIA_ENDPOINT, target_type, match_making_property,
                                         requested_property, l_values, missing_value, language=language,
                                         log_name=log_name)
    return retlist, retdict
