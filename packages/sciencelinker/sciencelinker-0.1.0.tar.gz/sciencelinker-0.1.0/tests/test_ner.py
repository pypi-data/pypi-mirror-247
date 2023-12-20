from sciencelinker import ner_dbpspot

SAMPLE_TEXT = '''
reStructuredText is the default plaintext markup language used by Sphinx. This section is a brief introduction to reStructuredText (reST) concepts and syntax, intended to provide authors with enough information to author documents productively. Since reST was designed to be a simple, unobtrusive markup language, this will not take too long.
'''

SAMPLE_URL = 'https://www.gesis.org/en/research/external-funding-projects/details/project/116/a-framework-for-finding-linking-and-enriching-social-science-linked-data'

l_annotations = ner_dbpspot.ner_spotlight_text([SAMPLE_TEXT], 'en')
print(l_annotations)
if len(l_annotations) == 1 and len(l_annotations[0]) == 7:
    print('Test OK')
else:
    print('Test failed')

# l_annotations = ner_dbpspot.ner_spotlight_url(['http://blog.fefe.de/'], 'de')
# print(l_annotations)
# if len(l_annotations) == 1 and len(l_annotations[0]) == 7:
#     print('Test OK')
# else:
#     print('Test failed')

# s = log.write_log(output_format='json')
# print(s)
