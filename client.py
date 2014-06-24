"""
Module for the client side of the recomender system application of source prioritization.

Functions :
kw_th
doc_categorize
main
"""

import content_extractor, TextRank, operator, os
import categorizer
import server
import math
import globalsfile as gl

def kw_th(t):
    """
        Takes time as an input and outputs the threshold which should be set on the number of keywords sent to server.
        Default : Shifted scaled sigmoid function.
    """
   
    return int(math.floor(30/(1+math.exp(-(t-15)/3))))

def doc_categorize(fsort):
    """
        Takes the keywords of the document with respective priorities and returns the document priority.

        Input :
            fsort - sorted list of (keywords, priority) tuples with respect to the proirity.

        Output :
            cat_probs - array of probabilities of the document of being of the perticular category.
    """
    cat_prob = [0,0,0,0]
    for term in fsort:
        print term[0]
    for kw in fsort:
        term_corr = [kw[1]*term for term in categorizer.categorize(kw[0])]
        cat_prob = map(operator.add, cat_prob, term_corr)
        print 'cumulative probability :', cat_prob
    return cat_prob

def main(url, time = 15, log = None):
    """
        Main function for the client.

        Inputs:
            url - URL to fetch content from.
            time - time user spent on page (optional).
            log - log file name to store logging (optional).
    """
    if not log == None:
        log1 = log
        while True:
            if not os.path.exists(log1):
                os.makedirs(log1)
                break
            else : log1 = log1+'_'

    content = content_extractor.get_content(url)

    if not log == None:
        logFile = open(log1+'/metadata',"a")
        logFile.write("URL : "+url+"\n\n")
        logFile.write("Title : "+content['title']+"\n\n")
        logFile.write("Meta Desc. : "+content['meta']+"\n\n")
        logFile.write("Content : "+content['content'].encode("utf8")+"\n\n")
        logFile.close()

    d = TextRank.text_rank(content['content'])
    sortd = sorted(d.iteritems(), key = operator.itemgetter(1), reverse=True)

    if not log == None:
        logtext = open(log1+'/textrank_result',"a")
        logtext.write(str(sortd))
        logtext.close()
 
    #final=[]
    #for i in sortd:
    #    for j in range(len(server.source_prob)):
    #        final.append((i[0], j, i[1]*server.source_prob[j]))
    #fsort = sorted(final, key = operator.itemgetter(2), reverse=True)
    #logres = open(log1+'/result',"a")
    #logres.write(str(fsort))
    #logres.close()

    links = server.run_server(sortd[:kw_th(time)])
    for link in links:
        print link

    return links
 
if __name__ == "__main__":
    """
        Test for the module.
    """

    gl.init()
    #raw_input("Enter a name for the run : ")
    url = 'http://www.cbsnews.com/news/astronomer-bruce-woodgate-inventor-of-the-camera-used-on-hubble-telescope-has-died/'
    main(url, time = 5)
    #print doc_categorize(fsort[:10])
