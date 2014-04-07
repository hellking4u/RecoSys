'''
Modules to test the functions of utilities.

Function:
dummy_ini
test_update
test_corpus_probs_update
'''

import utilities
import numpy as np
import random

def dummy_ini(log):
    """
        Dummy initialization for testing the update module.
        'log' is the name of file in which log should be saved.

        Other used variables -
        N = Number of sources
        N_obs = Number of keywords
    """
    N, N_obs = 3, 10
    logFile = open(log,'a')
    print >>logFile, 'Initialization of source keyword matrix with random values.'
    print >>logFile, 'Number of sources = 3'
    print >>logFile, 'Number of keywords = 10'
    logFile.close()
    return [np.random.uniform(0,1,N_obs) for i in range(N)], np.array([1.0/N for i in range(N)])

def test_update():
    data, source_probs = dummy_ini('test_init.log')
    print "Initial priorities : ",
    print source_probs
    print "Updating based on data : ",
    print data
    source_probs = utilities.update(source_probs, data, 0, 'test_update.log')
    print "Final priorities (with smoothing factor 0) : ",
    print source_probs

def test_corpus_probs_update(file_list,mode_of_operation = 2, return_term=1):
    f1 = open(file_list[0], "r").read().lower()
    f2 = open(file_list[1], "r").read().lower()
    f3 = open(file_list[2], "r").read().lower()
    return tfidf([1/3,1/3,1/3],[f1,f2,f3], 'test_corpus_probs_update.log',mode_of_operation, return_term)

#if __name__=="__main__":
#    test_corpus_probs_update(["test_corpus_file_1.txt", "test_corpus_file_2.txt","test_corpus_file_3.txt"], mode_of_operation = 2, return_term=0)
