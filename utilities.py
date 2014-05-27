"""
Module for computing knowledge source prioritization.

Function:
order_rating
update
corpus_words_dict
dict2term_doc_matx
raw2tfidf
textrank
tfidf
"""

import numpy as np, operator, re, math
import nltk
import TextRank
import rake as rk

def order_rating(probs,cumm_probs):
    """
        Return some similarity measure between 'probs' and 'cumm_probs'.
        Defualt : cosine distance
    """
    #order = sorted(range(len(cumm_probs)),key = lambda i:cumm_probs[i],reverse=True)
    #p, t = 1, 1
    #for n in order:
    #   p=p*probs[n]/t
    #   t=t-probs[n]
    #return p
    return probs.dot(cumm_probs)

def update(source_probs, data, lambd = 0, log = None):
    """
        Returns the updated priorities based on initial priorities ('source_probs') and term-source matrix ('data').
        'lambd' is the smoothing factor.
        'log' is the name of file in which log should be saved.

        Other used variables -
        'N' is Number of sources
        'N_obs' is Number of keywords
    """
    if not log == None:
        logFile = open(log,'a')
        print >>logFile,'Initial Probabilities - ', source_probs

    N = len(data)
    N_obs = len(data[0])
    probs = [d*np.count_nonzero(d)/float(d.sum()) if not float(d.sum()) == 0 else np.zeros(N_obs) for d in data]    #Normalizing the priorities.
    print probs

    cumm_probs = reduce(lambda a,b:map(operator.add,a,b),[np.multiply(source_probs[i],probs[i]) for i in range(N)])   #Computing the cummulative priorities
    temp = np.array([order_rating(probs[i],cumm_probs) for i in range(N)])

    if not log == None:
        print >>logFile,'Final Probabilities - ', source_probs
        logFile.close()

    return [lambd*source_probs[i]+(1-lambd)*np.divide(temp,temp.sum())[i] for i in range(N)]

def corpus_words_dict(strings):
    '''
        Takes a list of strings ('strings') as input and returns a dictionary ('dictio') with words used in string as keys and their raw counts as values.

        Example :
        >>> corpus_words_dict(['My name is Ajoy.', 'I do not care what your name is.'])
        {'ajoy': array([1, 0], dtype=uint8),
         'name': array([1, 1], dtype=uint8),
         'i': array([0, 1], dtype=uint8),
         'the': array([1, 1], dtype=uint8),
         'my': array([1, 0], dtype=uint8),
         'care': array([0, 1], dtype=uint8)}
        >>> 
    '''
    dictio = {}                  #Initialized the dictionary

    for j in range(len(strings)):
        check_list = ['the']
        for word in re.findall("[a-zA-Z']+", strings[j]):
            if word not in nltk.corpus.stopwords.words('english'):
                check_list.append(word)
        for i in check_list:
            temp = i.lower()
            if dictio.has_key(temp) :
                dictio[temp][j] = dictio[temp][j] + 1
            else :
                dictio[temp] = np.zeros(len(strings), dtype=np.uint8)
                dictio[temp][j] = 1

    return dictio

def dict2term_doc_matx(dictio):
    '''
        Takes the dictionary (similar as the output of corpus_words_dict) and returns the values and keys in the form of an matrix.

        Example :
        >>> dict2term_doc_matx(corpus_words_dict(['My name is Ajoy.', 'I do not care what your name is.']))
        array([[1, 1, 0, 1, 1, 0],
               [0, 1, 1, 1, 0, 1]], dtype=uint8)
        >>>
    '''
    return np.array(dictio.values()).T

def raw2tfidf(data, mode=0):
    """
        Takes the term-doc matrix ('data') as input and returns a matrix of same size but tf-idf values as elements.

        Options : 'mode' denotes the type of tf-idf to be used.
        0 - Raw Freqency(rf) (Default)
        1 - binary term frequency(btf)
        2 - augmented(atf)
        3 - logarithms(ltf)

        Other used variables -
        'N' is Number of sources
        'N_obs' is Number of keywords
    """
    N = len(data)
    N_obs = len(data[0])
    btf, ltf, atf = np.empty((N, N_obs)), np.empty((N, N_obs)), np.empty((N, N_obs))

    for i in range(N):              # ith document
        for j in range(N_obs):      # jth term
            if data[i][j] > 0: btf[i][j] = 1
            else: btf[i][j] = 0
            ltf[i][j] = math.log(float(data[i][j]+1))
            atf[i][j] = 0.5 + (0.5*data[i][j]/float(data[i].max()))
        df = np.sum(btf, axis=0)

    idf = np.array([float(N)/i for i in df])

    if mode == 0:
        return np.array([np.array(i)*idf for i in data])
    if mode == 1:
        return np.array([np.array(i)*idf for i in btf])
    if mode == 2:
        return np.array([np.array(i)*idf for i in ltf])
    if mode == 3:
        return np.array([np.array(i)*idf for i in atf])

def textrank(init_prob, strings, lambd = 0, log = None):
    """
        Returns the updated priorities based on initial priorities ('init_probs') and list of strings ('strings').
        Uses text rank to do so.
        'log' is the name of file in which log should be saved.
    """
    d = {}

    for j in range(len(strings)):                   #Merging the outputs of text rank applied on each string in strings.
        d1 = TextRank.text_rank(strings[j])
        for i in d1.keys():
            temp = i.lower()
            if d.has_key(temp) :
                d[temp][j] = d[temp][j] + d1[i]
            else :
                d[temp] = np.zeros(len(strings))
                d[temp][j] = d1[i]

    if not log == None:
        source_probs = update(init_prob, dict2term_doc_matx(d), lambd, log+"_update_results")
    else:
        source_probs = update(init_prob, dict2term_doc_matx(d), lambd, None)

    sorted_dict = sorted(d.iteritems(), key = lambda x: x[1].dot(np.array(source_probs)), reverse = True)

    if not log == None:
        logFile = open(log+'_sorted_dict','a')
        print >>logFile, sorted_dict
        logFile.close()

    return source_probs

def rake(init_prob, strings, lambd = 0, log = None):
    """
        Returns the updated priorities based on initial priorities ('init_probs') and list of strings ('strings').
        Uses Rake to do so.
        'log' is the name of file in which log should be saved.
    """
    d = {}

    for j in range(len(strings)):
        rake_instance = rk.RakeKeywordExtractor()                   #Merging the outputs of text rank applied on each string in strings.
        d1 = rake_instance.extract(strings[j])
        for i in d1.keys():
            temp = i.lower()
            if d.has_key(temp) :
                d[temp][j] = d[temp][j] + d1[i]
            else :
                d[temp] = np.zeros(len(strings))
                d[temp][j] = d1[i]

    if not log == None:
        source_probs = update(init_prob, dict2term_doc_matx(d), lambd, log+"_update_results")
    else:
        source_probs = update(init_prob, dict2term_doc_matx(d), lambd, None)

    sorted_dict = sorted(d.iteritems(), key = lambda x: x[1].dot(np.array(source_probs)), reverse=True)

    if not log == None:
        logFile = open(log+'_sorted_dict','a')
        print >>logFile, sorted_dict
        logFile.close()

    return source_probs

def tfidf(init_prob, strings, lambd = 0, log = None, mode_of_operation = 0, return_term=0):
    """
        Returns the updated priorities based on initial priorities ('init_probs') and list of strings ('strings').
        Uses tf-idf to do so.
        'log' is the name of file in which log should be saved.
        Mode of Operation :
        0 - Raw Freqency(rf) (Default)
        1 - binary term frequency(btf)
        2 - augmented(atf)
        3 - logarithms(ltf)
    """
    d = corpus_words_dict(strings)
    reduced = sorted(d.items(), key = lambda x: sum(x[1]),reverse = True)
    #data = dict2term_doc_matx(d)                               #raw freq data
    data = raw2tfidf(dict2term_doc_matx(d), mode_of_operation)  #tf-idf data

    ##print "Initial priorities : ",
    ##print source_probs
    if not log == None:
        source_probs = update(init_prob, data, lambd, log+"_update_results")
    else:
        source_probs = update(init_prob, data, lambd, None)
    ##print "Final priorities (with smoothing factor 0) : ",
    ##print source_probs
    
    counter = 0
    final_dict = {}
    for term in d.keys():
        final_dict[term] = data[return_term][counter]
        counter +=1
    sorted_dict = sorted(final_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    if not log == None:
        logFile = open(log+'_sorted_dict','a')
        print >>logFile, sorted_dict
        logFile.close()

    return source_probs


if __name__ == '__main__':
    print "test"
    rake_instance = rk.RakeKeywordExtractor()                   #Merging the outputs of text rank applied on each string in strings.
    d1 = rake_instance.extract("""
Compatibility of systems of linear constraints over the set of natural 
numbers. Criteria of compatibility of a system of linear Diophantine 
equations, strict inequations, and nonstrict inequations are considered. 
Upper bounds for components of a minimal set of solutions and algorithms 
of construction of minimal generating sets of solutions for all types of 
systems are given. These criteria and the corresponding algorithms for 
constructing a minimal supporting set of solutions can be used in solving 
all the considered types of systems and systems of mixed types.
  """)
    print d1
 
