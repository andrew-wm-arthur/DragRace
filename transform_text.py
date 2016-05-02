#!/bin/python/

''' feature_join.py

    Process the 
    
'''

import sys
import numpy as np
import sklearn as sk
from random import shuffle
from gensim import corpora, models, matutils, utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield LabeledSentence(doc,['PostID_%s' % (self.labels_list[idx])])


def LSI_transform( feature_list, num_topics ):

    for (corp, vocab, name) in feature_list:
        tf_idf = models.TfidfModel( corp )
        corpus_tfIdf = tf_idf[corp]

        LSI = models.LsiModel( corpus_tfIdf, id2word=vocab, num_topics=num_topics )
        # apply the LDA transformation 
        # convert from sparse to dense
        # save the matrix to disk
        np.save( name+'/'+name+'_LSI.npy', 
                 np.transpose( matutils.corpus2dense(LSI[corpus_tfIdf], num_topics))
               )
    

    #using this tutorial: https://medium.com/@klintcho/doc2vec-tutorial-using-gensim-ab3ac03d3a1#.ymtcbtlk2
    #and this ref: https://linanqiu.github.io/2015/10/07/word2vec-sentiment/
def doc2vec():
    postids = np.load("fixed_width/postids.npy")
   
    titles = np.load("title/title.npy")
    title_it = LabeledLineSentence(titles, postids)

    bodies = np.load("body/bodies.npy")
    body_it = LabeledLineSentence(bodies,postids)

    #see param docs: http://radimrehurek.com/gensim/models/doc2vec.html
    #need to fine-tune on a larger sub-sample
    title_model = Doc2Vec(size=200, window=10, min_count=10, alpha=.025, min_alpha=.025)
    title_model.build_vocab(title_it)

    body_model = Doc2Vec(size=200, window=10, min_count=10, alpha=.025, min_alpha=.025)
    body_model.build_vocab(body_it)

    for epoch in range(10):
        title_model.train(title_it)
        title_model.alpha -= .002
        title_model.min_alpha = title_model.alpha
        
        body_model.train(body_it)
        body_model.alpha -= .002
        body_model.min_alpha = body_model.alpha

    title_model.save("title/doc2vec.title_model")
    np.save("title/title_vecs.npy", (title_model.docvecs))
    body_model.save("body/doc2vec.body_model")
    np.save("body/body_vecs.npy", (body_model.docvecs))

    return(title_model, body_model)

def main():
    titleVocab = corpora.Dictionary.load("title/title_vocab.dict")
    titleCorpus = corpora.MmCorpus("title/title_word_corpus.mm")
    bodyVocab = corpora.Dictionary.load("body/body_vocab.dict")
    bodyCorpus = corpora.MmCorpus("body/body_word_corpus.mm")
    tagsVocab = corpora.Dictionary.load("tags/tags_vocab.dict")
    tagsCorpus = corpora.MmCorpus("tags/tags_word_corpus.mm")

    ''' hacky way to iterate over the corpora '''
    feature_list = [ ( titleCorpus, titleVocab, "title" ),
                     ( bodyCorpus, bodyVocab, "body" ),
                     ( tagsCorpus, tagsVocab, "tags" ) ]

    LSI_transform( feature_list, num_topics=50 )



if __name__ == '__main__':
    title_model, body_model = doc2vec()

    #inspect model performance
    '''
    print(body_model.doesnt_match("trouble issue problem python".split()))
    print(body_model.doesnt_match("html css compiler".split()))
    print(body_model.most_similar("javascript"))
    print(body_model.infer_vector("html test code problem".split()))
    print(body_model.similarity('html','css'))
    print(body_model.similarity('java','java'))
    print(body_model.similarity('compiler','python'))
    print(body_model.docvecs[0])
    print(body_model.docvecs['PostID_4'])
    print(body_model.docvecs.most_similar('PostID_4'))
    print(body_model.docvecs.most_similar('PostID_16114'))
    '''



