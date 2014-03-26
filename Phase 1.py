__author__ = 'nikhil'
import gurmeet
import numpy as np
import random, math
import search_module as sm 
# NOTE : Always import the search module AFTER any pygraph import (gurmeet.py imports pygraph)
#        This is due to the fact that pygraph does some unnessary package checks.

def phase1_update(source_prob, wiki_list, keywords, n_iter, verbosity, mode_of_operation):
        
        logfile = open("test_2.txt","a")
        for kw in keywords:
                wiki_content = sm.get_wiki_article(kw, verbose=verbosity, search_list=[w[1] for w in wiki_list])
                print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
                [source_prob, sorted_list] = gurmeet.textrank(source_prob, wiki_content)

                print "\n\n---------\n"
                logfile.write(kw)
                for i in range(len(source_prob)):
                        print wiki_list[i][0], source_prob[i]/source_prob[0], "actual (", source_prob[i],")"
                        logfile.write(wiki_list[i][0]+" "+str(source_prob[i]/source_prob[0])+"actual ( "+str(source_prob[i])+" )")
                
        #tr_list = TextRank.text_rank(wiki_content[0])
        return source_prob, sorted_list

def key_wiki_err(keywords, wiki_list, k, n, n_iter, mode_of_operation):
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        s = np.empty((n, N))
        for i in range(n):
                random.shuffle(keywords)
                s[i], sorted_list = phase1_update(source_prob, [w[1] for w in wiki_list], keywords[:k], n_iter, False, mode_of_operation)
        t1, t2 = np.empty(N), np.empty(N)
        for t in s:
                for i in range(N):
                        t1[i] = t1[i] + t[i]
                        t2[i] = t2[i] + t[i]*t[i]
        sigma = np.empty(N)
        norm2 = 0

        for i in range(N):
                sigma[i] = t2[i]/N - (t1[i]/N)**2
                norm2 = norm2 + sigma[i]*sigma[i]
        return math.sqrt(norm2)

def test_run():
        verbosity = True
        keywords = ["Delhi", "dog", "mars", "atom"]
        wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com")]
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        mode_of_operation = 2
        [source_prob, sorted_list] = phase1_update(source_prob, wiki_list, keywords, 2, verbosity, mode_of_operation)
        
        print "The top 15 keywords :"
        for g, v in sorted_list[:15]:
                print g, v,
                print '\t',
        print "\n\n---------\n"
        for i in range(len(source_prob)):
                print wiki_list[i][0], source_prob[i]/source_prob[0], "actual (", source_prob[i],")"
        
        #print key_wiki_err(keywords, [w[1] for w in wiki_list], 2, 3, 2, mode_of_operation)

if __name__ == "__main__":
        test_run()
