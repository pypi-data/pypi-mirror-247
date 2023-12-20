import pandas as pd
from sciencelinker import kg_wikidata
from sciencelinker import processing_log as log

df_data = pd.read_csv('../test-datasets/artificial_dataset_1.csv')

print(df_data['BEFR.: STAATSBUERGERSCHAFT 1'].values)

l_types = kg_wikidata.lookup_types(df_data['BEFR.: STAATSBUERGERSCHAFT 1'], language='de')
for i in range(min(len(l_types), 100)):
    print(str(i) + ' ' + str(l_types[i]))

requested_type = l_types[0][0]
identifying_property = l_types[0][1]

l_props = kg_wikidata.lookup_properties(requested_type, identifying_property, df_data['BEFR.: STAATSBUERGERSCHAFT 1'], language='de')
if len(l_props) == 0:
    print('No properties found')
for i in range(min(len(l_props), 100)):
    print(str(i) + ' ' + str(l_props[i]))

requested_property = l_props[30][0]  # P1082 Population

l_new_data, d = kg_wikidata.enrich(requested_type, identifying_property, requested_property,
                                   df_data['BEFR.: STAATSBUERGERSCHAFT 1'], language='de', missing_value='missing')
print(d)
print(len(d))
if len(d) == 27:
    print('Test OK')
else:
    print('Test failed')

# s = log.write_log(output_format='json')
# print(s)
