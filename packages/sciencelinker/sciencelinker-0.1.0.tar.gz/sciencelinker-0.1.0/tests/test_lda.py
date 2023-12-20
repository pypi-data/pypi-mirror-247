from sciencelinker import lda_gensim
from sciencelinker import processing_log as log
import lda.datasets

titles = lda.datasets.load_reuters_titles()

titles_pp = lda_gensim.preprocess_texts(titles)

topics = lda_gensim.get_topics(titles_pp)

for topic in topics:
    print(topic)

if len(topics) == 10:
    print('Test OK')
else:
    print('Test failed')

# s = log.write_log(output_format='json')
# print(s)
