__author__ = 'gurmeet'

import numpy as np
import random, math
import os, sys
sys.path.insert(0, '../')
import utilities
import search_module as sm

def test3(source_prob, wiki_list, keywords, n_iter, verbosity, mode_of_operation, log, x):
        j=0
        logFile = open(log+'_intermediate_probs',"a")
        for kw in keywords:
                j = j+1
                wiki_content = sm.get_wiki_article(kw, verbose=verbosity, search_list=[w[1] for w in wiki_list])
                if x == 1:
                    wiki_content[2] = wiki_content[2]+wiki_content[1]
                logwiki = open(log+"_"+kw+"_wiki_contents","a")
                for n in range(len(wiki_content)):
                        logwiki.write(wiki_list[n][0]+' :\n')
                        logwiki.write(wiki_content[n].encode("utf8")+'\n\n\n')
                logwiki.close()
                print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
                if mode_of_operation == 4:
                        source_prob = utilities.textrank(source_prob, wiki_content, log+'_'+str(j)+'_'+kw)
                else:
                        source_prob = utilities.tfidf(source_prob, wiki_content, log+'_'+str(j)+'_'+kw, mode_of_operation=mode_of_operation, return_term=0)
                print "\n\n---------\n"
                for i in range(len(source_prob)):
                        logFile.write(wiki_list[i][0]+" : "+str(source_prob[i]/source_prob[0])+'\n')
        logFile.close()
        logoutput = open(log,"a")
        logoutput.write("Source Probs : "+ str(source_prob)+'\n')
        logoutput.close()
        #tr_list = TextRank.text_rank(wiki_content[0])
        return source_prob

def test_run(log, x):
        if not os.path.exists(log):
                os.makedirs(log)
        logFile = open(log+'/metadata','a')
        verbosity = True
        logFile.write('Verbosity = '+ str(verbosity))
        keywords = ["atom"]
        logFile.write('keywords = '+ str(keywords))
        wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com")]
        logFile.write('Wiki List = '+ str(wiki_list))
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        logFile.write('Initial source probabilities = '+ str(source_prob))
        mode_of_operation = 4
        logFile.write('Mode of operation = ' + str(mode_of_operation))
        source_prob = test3(source_prob, wiki_list, keywords, 2, verbosity, mode_of_operation, log+'/'+log, x)
        for i in range(len(source_prob)):
                print wiki_list[i][0], source_prob[i]/source_prob[0], "Original : (", source_prob[i], ")"
        
        #print key_wiki_err(keywords, [w[1] for w in wiki_list], 2, 3, 2, mode_of_operation)

if __name__ == "__main__":
        test_run('test_A', 0)
        print
        print "Running the second iteration of test.."
        print
        test_run('test_AB', 1)
