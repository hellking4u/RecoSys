__author__ = 'nikhil'
import search_module as sm
import gurmeet
import numpy as np
import random, math

def phase1_update(source_prob, wiki_list, keywords, n_iter, verbosity, mode_of_operation):
        for kw in keywords:
                wiki_content = sm.get_wiki_article(kw, verbose=verbosity, search_list=wiki_list)
                print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
                [source_prob, sorted_list] = gurmeet.tfidf(source_prob, wiki_content, mode_of_operation=mode_of_operation, return_term=0)
                print "\n\n---------\n"
                for i in range(len(source_prob)):
                        print wiki_list[i], source_prob[i]/source_prob[0]
                
        #tr_list = TextRank.text_rank(wiki_content[0])
        return source_prob, sorted_list

def key_wiki_err(keywords, wiki_list, k, n, n_iter, mode_of_operation):
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        s = np.empty((n, N))
        for i in range(n):
                random.shuffle(keywords)
                s[i], sorted_list = phase1_update(source_prob, wiki_list, keywords[:k], n_iter, False, mode_of_operation)
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
        #keywords = ["Delhi"]
        wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com")]
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        mode_of_operation = 2
        [source_prob, sorted_list] = phase1_update(source_prob, [w[1] for w in wiki_list], keywords, 2, verbosity, mode_of_operation)
        
        print "The top 15 keywords :"
        for g, v in sorted_list[:15]:
                print g, v,
                print '\t',
        print "\n\n---------\n"
        for i in range(len(source_prob)):
                print wiki_list[i][0], source_prob[i]/source_prob[0]
        
        #print key_wiki_err(keywords, [w[1] for w in wiki_list], 2, 3, 2, mode_of_operation)

if __name__ == "__main__":
        test_run()
