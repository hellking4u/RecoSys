__author__ = 'nikhil'
"""
Module for the TextRank Algorithm.
TextRank is based on Google's PageRank Algorithm, this models text as a sparse graph
and utilizes the PageRank Algorithm to find relative term weights.

Dependencies :

* pygraph (use easy_install or PyCharm to install)

From this paper: http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf
"""
import nltk
import itertools
from operator import itemgetter
import wikipedia, sys, string

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.pagerank import pagerank
from pygraph.classes.exceptions import AdditionError

def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
    return [item for item in tagged if item[1] in tags]


def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def begin_test(kw):
    """
    TODO : Improve model performance.
    """
    print "Begin TextRank Algorithm with keyword set",
    print kw
    for keyword in kw:
        page_title = keyword
        ny = wikipedia.page(page_title)
        print "Reading from wikipedia...",
        text = ny.content#.encode('utf-8', errors='replace')
        print "done"
        print "------------Page Summary------------\n"
        print wikipedia.summary(page_title,3).encode('utf-8', errors='replace')
        print "------------End Summary------------\n"
        print "------------Begin TextRank algorithm------------\n"
        op = text_rank(text);
        print op

def text_rank(text):
    text = text.lower()
    stop_words = nltk.corpus.stopwords.words('english')
    stop_set = stop_words + list(string.punctuation)
    list_text = [i for i in text.split(" ") if i not in stop_set]
    text = " ".join(list_text)
    text = nltk.word_tokenize(text)

    tagged = nltk.pos_tag(text)


    tagged = filter_for_tags(tagged)
    tagged = normalize(tagged)

    unique_word_set = unique_everseen([x[0] for x in tagged])

    gr = digraph()
    gr.add_nodes(list(unique_word_set))

    window_start = 0
    window_end = 2

    while 1:

        window_words = tagged[window_start:window_end]
        if len(window_words) == 2:
            #print window_words
            pass
            try:
                gr.add_edge((window_words[0][0], window_words[1][0]))
            except AdditionError, e:
                #print 'already added %s, %s' % ((window_words[0][0], window_words[1][0]))
                pass
        else:
            break

        window_start += 1
        window_end += 1
    calculated_page_rank = pagerank(gr)
    di = sorted(calculated_page_rank.iteritems(), key=itemgetter(1), reverse=True)
    return di
    #for k, g in di:
        #print k, g
if __name__=="__main__":
    kw_list = ["New York", "Boston"]
    begin_test(kw_list)