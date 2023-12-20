import pandas as pd

from sciencelinker import kg_dbpedia
from sciencelinker import processing_log as log

df_data = pd.read_csv('../test-datasets/artificial_dataset_2.csv')

print(df_data['COUNTRY/SAMPLE ID (SERIES STANDARD)'].values)

l_types = kg_dbpedia.lookup_types(df_data['COUNTRY/SAMPLE ID (SERIES STANDARD)'].values, language='en')
for i in range(min(len(l_types), 100)):
    print(str(i) + ' ' + str(l_types[i]))

requested_type = l_types[2078][0]
identifying_property = l_types[2078][1]

l_props = kg_dbpedia.lookup_properties(requested_type, identifying_property, df_data['COUNTRY/SAMPLE ID (SERIES STANDARD)'], language='en')
for i in range(min(len(l_props), 100)):
    print(str(i) + ' ' + str(l_props[i]))

requested_property = l_props[37][0]

l_new_data, d = kg_dbpedia.enrich(requested_type, identifying_property, requested_property, df_data['COUNTRY/SAMPLE ID (SERIES STANDARD)'],
                                  missing_value='missing', language='en')
print(d)

if len(d) == 24:
    print('Test OK')
else:
    print('Test failed')

# s = log.write_log(output_format='json')
# print(s)
