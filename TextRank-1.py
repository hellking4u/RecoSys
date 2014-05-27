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
import string
from operator import itemgetter

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.pagerank import pagerank
from pygraph.classes.exceptions import AdditionError
from pygraph.readwrite.dot import write
import sys

# Windows -
import graphviz as gv

# Unix -
#sys.path.append('..')
#sys.path.append('/usr/lib/graphviz/python/')
#sys.path.append('/usr/lib64/graphviz/python/')
#import gv

def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
    return [item for item in tagged if item[1] in tags]


def normalize(tagged):
    x = [(item[0].replace('.', ''), item[1]) for item in tagged]
    return x


def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen."""
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
    print "Begin TextRank Algorithm with sample string",
    print kw
    return text_rank(kw)

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
    #di = sorted(calculated_page_rank.iteritems(), key=itemgetter(1), reverse=True)
    render = True
    if (render):
        dot = write(gr)
        gvv = gv.readstring(dot)
        gv.layout(gvv,'dot')
        gv.render(gvv,'png','textrank.png')
    return calculated_page_rank
    #for k, g in di:
        #print k, g

if __name__ == "__main__":
    test_string = "New York is a state in the Northeastern and Mid-Atlantic regions of the United States. New York is the 27th-most extensive, the third-most populous, and the seventh-most densely populated of the 50 United States. New York is bordered by New Jersey and Pennsylvania to the south and by Connecticut, Massachusetts, and Vermont to the east. "
    print begin_test(test_string)
