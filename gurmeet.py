"""
Module for computing knlwledge source prioritiztion based on bayesian statistics

Functional Usage :

"""
__author__ = 'gurmeet'
import numpy as np, random, operator, re, math, wikipedia
import nltk
def order_rating(probs,cumm_probs):
    """
        
    """
    #order = sorted(range(len(cumm_probs)),key = lambda i:cumm_probs[i],reverse=True)
    #p, t = 1, 1
    #for n in order:
    #   p=p*probs[n]/t
    #   t=t-probs[n]
    #return p
    return probs.dot(cumm_probs)

def update(source_probs, data, l):
    logFile = open("logfile.log",a)
    print >>logFile,source_probs
    logFile.close()
    N = len(data)
    N_obs = len(data[0])
    probs = [d/float(d.sum()) for d in data]
    cumm_probs = reduce(lambda a,b:map(operator.add,a,b),[np.multiply(source_probs[i],probs[i]) for i in range(N)])
    temp = np.array([order_rating(probs[i],cumm_probs) for i in range(N)])
    return [l*source_probs[i]+(1-l)*np.divide(temp,temp.sum())[i] for i in range(N)]

def dummy_ini():
    """
        N = Number of sources
        N_obs = Number of keywords
    """
    N, N_obs = 3, 10
    return [np.random.uniform(0,1,N_obs) for i in range(N)], np.array([1.0/N for i in range(N)])

def test_update():
    data, source_probs = dummy_ini()
    print "Initial priorities : ",
    print source_probs
    print "Updating based on data : ",
    print data
    source_probs = update(source_probs, data, 0)
    print "Final priorities (with smoothing factor 0) : ",
    print source_probs

def words_dict(s):
    d = {}
    for i in re.findall("[a-zA-Z']+",s):
        temp = i.lower()
        if d.has_key(temp) : d[temp] = d[temp] + 1
        else : d[temp] = 1
    return d

def sorted_words_rf(d):
    return sorted(d.items(), key = lambda x: x[1], reverse = True)

def test_words_rf():
    f = open("dog.txt","r")
    d = sorted_words_rf(words_dict(f.read()))
    print d[:100]
    f.close()

def corpus_words_dict(s):
    d = {}
    for j in range(len(s)):
        check_list = ['the']
        for word in re.findall("[a-zA-Z']+",s[j]):
            if word not in nltk.corpus.stopwords.words('english'):
                check_list.append(word)
        for i in check_list:
            temp = i.lower()
            if d.has_key(temp) :
                d[temp][j] = d[temp][j] + 1
            else :
                d[temp] = np.zeros(len(s), dtype=np.uint8)
                d[temp][j] = 1
    return d

def dict2term_doc_matx(d):
    return np.array(d.values()).T

def raw2tfidf(data,mode=0):
    """
    0 - Raw Freqency
    btf - binary term frequency
    atf - augmented
    ltf - logarithms
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
    

def tfidf(init_prob, a,b,c,mode_of_operation = 2, return_term=1):
    """
    Mode of Operation :
    0 - Raw Freqency
    1 - btf - binary term frequency
    2 - ltf - logarithms
    3 - atf - augmented
    """
    d = corpus_words_dict([a, b, c])
    reduced = sorted(d.items(), key = lambda x: sum(x[1]),reverse = True)
    #data = dict2term_doc_matx(d)               #raw freq data
    raw_data = raw2tfidf(dict2term_doc_matx(d),2)
    data = raw2tfidf(raw_data, 3)   #tf-idf data
    counter = 0
    final_dict = {}
    for term in d.keys():
        final_dict[term] = data[return_term][counter]
        counter +=1
    sorted_dict = sorted(final_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    ##print "Initial priorities : ",
    ##print source_probs
    source_probs = update(init_prob, data, 0)
    ##print "Final priorities (with smoothing factor 0) : ",
    ##print source_probs

    return [source_probs,sorted_dict]

def test_corpus_probs_update(file_list,mode_of_operation = 2, return_term=1):
    f1 = open(file_list[0], "r").read().lower()
    f2 = open(file_list[1], "r").read().lower()
    f3 = open(file_list[2], "r").read().lower()
    return tfidf(f1,f2,f3,mode_of_operation, return_term)

if __name__=="__main__":
    test_corpus_probs_update(["test_corpus_file_1.txt", "test_corpus_file_2.txt","test_corpus_file_3.txt"], mode_of_operation = 2, return_term=0)
