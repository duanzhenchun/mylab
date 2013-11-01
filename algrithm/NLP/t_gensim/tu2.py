#Transformation interface
from gensim import corpora, models, similarities


dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
corpus = corpora.MmCorpus('/tmp/deerwester.mm')
print corpus

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

#Transforming vectors
doc_bow = [(0, 1), (1, 1)]
print tfidf[doc_bow]  # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc

for choice in (models.LsiModel, models.LdaModel):
    model = choice(corpus_tfidf, id2word=dictionary, num_topics=2) 
    corpus_mod = model[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    fname = '/tmp/%s' % repr(choice) 
    model.save(fname)  # same for tfidf, lda, ...
    model = choice.load(fname)

    # topic
    model.print_topics(2)
    for doc in corpus_mod:  # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
        print doc

    # test example
    doc = "Human computer interaction"
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_mod = model[vec_bow]  # convert the query to MODEL space
    print vec_mod

    # Initializing query structures
    index = similarities.MatrixSimilarity(model[corpus])  # transform corpus to MODEL space and index it
    index.save('/tmp/deerwester.index')
    index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
    
    # Performing queries
    sims = index[vec_mod]  # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item:-item[1])
    print sims  # print sorted (document number, similarity score) 2-tuples
