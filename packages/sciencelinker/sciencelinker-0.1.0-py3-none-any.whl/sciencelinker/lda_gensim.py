import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

from . import processing_log as log


def preprocess_texts(l_text: str, language: str = 'english', log_name: str = 'default') -> list:
    """Performs preprocessing for topic modelling.

    :param l_text: List of documents to be processed
    :type l_test: str
    :param language: Language to use
    :type language: str
    :param log_name: Name of the log to use
    :type log_name: str
    :return: list of preprocessed documents
    :rtype: list of strings
    """
    in1 = log.DataItem('l_text', l_text, 'List of documents to be preprocessed')
    in2 = log.DataItem('language', language, 'The language to use')
    log.start_procedure(name='Preprocessing for topic modeling', l_inputs=[in1, in2],
                        method_url='http://sciencelinker.git.gesis.org/docs/lda_gensim.html', log_name=log_name)

    l_results = []
    for text in l_text:
        processed_text = simple_preprocess(text, deacc=True)
        l_results.append(processed_text)
    out = log.DataItem('l_results', l_results, 'The preprocessed documents')
    log.end_procedure([out], log_name=log_name)
    return l_results


def get_topics(l_text: str, log_name: str = 'default') -> list:
    """Perform topic modelling using Latent Dirichlet Allocation (LDA).

    :param l_text: Input documents, should be preprocessed
    :type l_text: list of str
    :param log_name: Name of the log to use
    :type log_name: str
    :return: List of top 10 topics represented through the most relevant words.
    :rtype: list of list of str
    """
    in1 = log.DataItem('l_text', l_text, 'Input text')
    log.start_procedure(name='Latent Dirichlet Allocation', l_inputs=[in1],
                        method_url='http://sciencelinker.git.gesis.org/docs/', log_name=log_name)
    id2word = corpora.Dictionary(l_text)
    corpus = []
    for text in l_text:
        new = id2word.doc2bow(text)
        corpus.append(new)

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=50,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto')
    l_topics = lda_model.top_topics(corpus=corpus)

    l_ret_topics = []
    for topic in l_topics[:10]:
        t = [tup[1] for tup in topic[0]]
        l_ret_topics.append(t)
    out1 = log.DataItem('l_ret_topics', l_ret_topics, 'List of topics')
    log.end_procedure([out1], log_name)
    return l_ret_topics
