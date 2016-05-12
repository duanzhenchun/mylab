#!/usr/bin/env python
# encoding: utf-8
# http://joshbohde.com/blog/document-summarization
"""
For a gift recommendation side-project of mine, I wanted to do some automatic summarization for products. A fairly easy way to do this is TextRank, based upon PageRank. In this example, the vertices of the graph are sentences, and the edge weights between sentences are how similar the sentences are.
"""

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from collections import Counter
import networkx as nx

document = """To Sherlock Holmes she is always the woman. I have
seldom heard him mention her under any other name. In his eyes she
eclipses and predominates the whole of her sex. It was not that he
felt any emotion akin to love for Irene Adler. All emotions, and that
one particularly, were abhorrent to his cold, precise but admirably
balanced mind. He was, I take it, the most perfect reasoning and
observing machine that the world has seen, but as a lover he would
have placed himself in a false position. He never spoke of the softer
passions, save with a gibe and a sneer. They were admirable things for
the observer-excellent for drawing the veil from men’s motives and
actions. But for the trained reasoner to admit such intrusions into
his own delicate and finely adjusted temperament was to introduce a
distracting factor which might throw a doubt upon all his mental
results. Grit in a sensitive instrument, or a crack in one of his own
high-power lenses, would not be more disturbing than a strong emotion
in a nature such as his. And yet there was but one woman to him, and
that woman was the late Irene Adler, of dubious and questionable
memory.
"""
document = ' '.join(document.strip().split('\n'))


def bag_of_words(sentence):
    return Counter(word.lower().strip('.,') for word in sentence.split(' '))


def textrank(document, top=3):
    sentence_tokenizer = PunktSentenceTokenizer()
    sentences = sentence_tokenizer.tokenize(document)

    bow_matrix = CountVectorizer().fit_transform(sentences)
    normalized = TfidfTransformer().fit_transform(bow_matrix)

    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    res = sorted(
        ((scores[i], i, s) for i, s in enumerate(sentences)),
        reverse=True)
    return res


def summary(document, top=3):
    res = textrank(document)
    # sort in doc order
    return ' '.join([i[2] for i in sorted(res[:top], key=lambda (i): i[1])])


def file_summary(fname):
    with open(fname, 'rb') as f:
        document = f.read().decode('utf8').replace('\r\n', '').replace(' ', '').strip()
        doc = document.replace(u'。', '. ')
        print summary(doc)

print summary(document)
for fname in ('./accountindex/data/pp_cs.txt', './bite.of.china/srt/第一集 自然的馈赠.txt'):
    file_summary(fname)
