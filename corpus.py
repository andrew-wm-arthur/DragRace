#!/bin/python/

'''
    Processes the output of the sqlite3 db
    Splits the data into postid, computed, views, title, body, tags

    Allows saving of parsed, raw text to load/transform down-stream

    Expected format of sql output:
        PostId, Reputation, UserLifeDays, PostLifeDays, 
        CodeSnippet, PostLength, URLCount, PostViewCount, 
        Title, Body, Tags, Delimiter='@$R$@' OR '0x1E'
'''

import sys
import math
import numpy as np
from gensim import corpora, models, matutils
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


def read_data( file_name ):
    with open( file_name, "r") as f:
        #use this return statement on final data - changed row delimiter to sqlite standard
        #return [ row.split("##C##") for row in f.read().split("0x1E")[:-1] ]
        return [ row.split("##C##") for row in f.read().split("@$R$@")[:-1] ]

def feature_split(data, postid_ind = 0, ci=(1,7), views_ind=7, title_ind=8, body_ind=9, tags_ind=10):
    '''
        Seperate the four feature categories to be transformed/processed 
        independently

        Indexes within data[] of each feature category are params
        'ci' for computed features indices

        @BUG one of the computed features is missing in Andy's sample
    '''
    postid = [ row[postid_ind].strip() for row in data]
    title = [ row[title_ind] for row in data]
    body = [ row[body_ind] for row in data]
    tags = [ row[tags_ind] for row in data]
    computed = [[ f.strip() for f in row[ ci[0]:ci[1] ]] for row in data ]
    views = [ row[views_ind] for row in data]

    return (postid, title, body, tags, computed, views)


def tokenize_words( text ):
    regex_tokenizer = RegexpTokenizer('[A-Z]\w+|[a-z]\w+')
    tokens = [regex_tokenizer.tokenize(row) for row in text]
    # stopwords = nltk.corpus.stopwords.words('english')

    # removing 60 most common English words from corpus
    # computing cluster wouldn't recognize stopwords
    stopwords = ['the','be','to','of','and','a','in','that','have','I','it','for',
                    'not','on','with','he','as','you','do','at','this','but','his',
                    'by','from','they','we','say','her','she','or','an','will','my',
                    'one','all','would','there','their','what','so','up','out','if',
                    'about','who','get','which','go','me','when','make','can','like',
                    'time','no','just','him','know','take']
    tokens =  [[token for token in row if token not in stopwords] for row in tokens]
    lowercase_tokens = [ [token.lower() for token in row] for row in tokens]
    return lowercase_tokens

def tag_split( tags ):
    tags = [[ x.strip('<>') for x in row.split('><') ] for row in tags ]
    return tags

def tag_prune(tags):
    tags = tag_split(tags)  
    tagsVocab = corpora.Dictionary( tags )
    # use all the tags
    allTagsCorpus = [ tagsVocab.doc2bow( p ) for p in tags ]
    tagsVocab.save( "tags/tags_vocab.dict" )
    corpora.MmCorpus.serialize( "tags/tags_word_corpus.mm", allTagsCorpus )
    # prune the vocabulary to the most common 10,000 tags
    tagsVocab.filter_extremes(0,1,keep_n = 10000)
    prunedTagsCorpus = [ tagsVocab.doc2bow( p ) for p in tags ]
    tagsVocab.save( "tags/prunedTags_vocab.dict" )
    corpora.MmCorpus.serialize( "tags/prunedTags_word_corpus.mm", prunedTagsCorpus )
    # creates a tag vector of len = 10,000 for each document
    prunedTags_vecs = np.transpose( matutils.corpus2dense( prunedTagsCorpus, 10000 ) )
    np.save("tags/prunedTags.npy", prunedTags_vecs )
    return(prunedTags_vecs)

def make_BOW( title, body, tags ):
    ''' 
        Take each textual feature and create a GenSim
        corpus and vocabulary from it. Serialize these
        to disk for later use.

        @BUG title, body, and tags are not in a consistent
            order in the sql output right now.
    '''
    ''' title '''
    title = tokenize_words( title )
    title.save("title/title.npy")
    titleVocab = corpora.Dictionary( title )
    titleCorpus = [ titleVocab.doc2bow( p ) for p in title ]
    titleVocab.save( "title/title_vocab.dict" )
    corpora.MmCorpus.serialize( "title/title_word_corpus.mm", titleCorpus )
    ''' body '''
    body = tokenize_words( body )
    bodyVocab = corpora.Dictionary( body )
    bodyCorpus = [ bodyVocab.doc2bow( p ) for p in body ]
    bodyVocab.save( "body/body_vocab.dict" )
    corpora.MmCorpus.serialize( "body/body_word_corpus.mm", bodyCorpus )
    ''' tags '''
    tags = tag_split( tags )    # rows = [ tags in a document ]
    tagsVocab = corpora.Dictionary( tags )
    # use all the tags
    allTagsCorpus = [ tagsVocab.doc2bow( p ) for p in tags ]
    tagsVocab.save( "tags/tags_vocab.dict" )
    corpora.MmCorpus.serialize( "tags/tags_word_corpus.mm", allTagsCorpus )
    # prune the vocabulary to the most common 10,000 tags
    tagsVocab.filter_extremes(0,1,keep_n = 10000)
    prunedTagsCorpus = [ tagsVocab.doc2bow( p ) for p in tags ]
    tagsVocab.save( "tags/prunedTags_vocab.dict" )
    corpora.MmCorpus.serialize( "tags/prunedTags_word_corpus.mm", prunedTagsCorpus )
    # creates a tag vector of len = 10,000 for each document
    prunedTags_vecs = np.transpose( matutils.corpus2dense( prunedTagsCorpus, 10000 ) )
    np.save("tags/prunedTags.npy", prunedTags_vecs )

def main():

    if( len(sys.argv) < 2 ):
        print("\tpass the path of the data text file")
        exit()
    
    data = read_data( sys.argv[1] )

    ( postid,
 	  title,
      body,
      tags,
      computed,
      views ) = feature_split(data)

    np.save("title/title.npy", np.array(tokenize_words(title)))
    np.save("body/bodies.npy", np.array(tokenize_words(body)))
    np.save("tags/tags.npy", np.array(tag_prune(tags)))
    np.save("fixed_width/postids.npy", np.array(postid))
    np.save("fixed_width/computed.npy", np.array(computed).astype(np.float))
    np.save("fixed_width/views.npy", np.array(views).astype(np.float))
    np.save("fixed_width/logviews.npy", np.log(np.array(views).astype(np.float)))
    #make_BOW( title, body, tags )

if __name__ == '__main__':
    main()