#!/bin/python/

''' feature_join.py

    computed features:
        Reputation
        UserLifeDays
        PostLifeDays
        CodeSnippet (binary)
        PostLength
        URLCount
'''

import sys
import math
from random import randint
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn import cross_validation
from gensim import corpora, models


def load_data( file_list ):
    title = np.load(file_list[0])
    body = np.load(file_list[1])
    tags = np.load(file_list[2])
    computed = np.load(file_list[3])
    views = np.load(file_list[4])

    return (np.hstack(( title,
                        body,
                        tags,
                        computed )),
                        views
            )

def regress( X, y, iterations = 10 ):
    ridge_model = Ridge( alpha=.1).fit(X,y)
    print("within sample R^2: "+str(ridge_model.score(X,y)))
    print('\n')

    linear_scores = []
    kernel_scores = []
    for i in range(iterations):
        ( X_train,
          X_test,
          y_train,
          y_test 
        ) = cross_validation.train_test_split( X, y, random_state=randint(0,100))

        model = Ridge( alpha=10.0 )
        model.fit(X_train,y_train)
        linear_scores.append(model.score(X_test,y_test))

    print ( 'linear scores:\tmean = '+
            str(np.average(linear_scores))+
            '\tstd dev = '+
            str(np.std(linear_scores))
          )

def main():
    #if( len(sys.argv) != 6 ):
        #print('\tpass the paths of the four feature files and the target:')
        #print('\t\ttitle body tags computedFeatures views')
        #exit()

    (X, y) = load_data(["title/title_vecs.npy", 
                        "body/body_vecs.npy", 
                        "tags/prunedTags.npy",
                        "fixed_width/computed.npy",
                         "fixed_width/logviews.npy"])
    #(X,y) = load_data( sys.argv[1:] )
    regress( X, y )

if __name__ == '__main__':
    main()