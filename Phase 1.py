import utilities
import numpy as np
import random, math
import os
import search_module as sm

def phase1_update(source_prob, wiki_list, keywords, n_iter, verbosity, log, mode_of_operation = 4):
        '''
            Compute and return the updated source priorities based on the initial priorities (source_prob) and the keywords.
            Can use text rank (default) as well as tf-idf to do so.
            'log' is the name of file in which log should be saved.
        '''
        j=0
        logFile = open(log+'_intermediate_probs',"a")
        for kw in keywords:
                j = j+1
                wiki_content = sm.get_wiki_article(kw, verbose=verbosity, search_list=[w[1] for w in wiki_list])  #Get the content of the web pages respected to each website for the keyword 'kw'
                logwiki = open(log+"_"+kw+"_wiki_contents","a")
                for n in range(len(wiki_content)):
                        logwiki.write(wiki_list[n][0]+' :\n')
                        logwiki.write(wiki_content[n].encode("utf8")+'\n\n\n')
                logwiki.close()
                if verbosity : print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
                if mode_of_operation == 4:
                        source_prob = utilities.textrank(source_prob, wiki_content, log+'_'+str(j)+'_'+kw)
                else:
                        source_prob = utilities.tfidf(source_prob, wiki_content, log+'_'+str(j)+'_'+kw, mode_of_operation=mode_of_operation, return_term=0)
                if verbosity : print "\n\n---------\n"
                for i in range(len(source_prob)):
                        if verbosity : print wiki_list[i][0], source_prob[i]/source_prob[0]
                        logFile.write(wiki_list[i][0]+" : "+str(source_prob[i]/source_prob[0])+'\n')
        logFile.close()
        logoutput = open(log,"a")
        logoutput.write("Source Probs : "+ str(source_prob)+'\n')
        logoutput.close()
        #tr_list = TextRank.text_rank(wiki_content[0])
        return source_prob

def key_wiki_err(keywords, wiki_list, k, n, n_iter, log, mode_of_operation):
        '''
            Compute and return the non-correlation between sites and the keywords.
            'log' is the name of file in which log should be saved.
        '''
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        s = np.empty((n, N))
        for i in range(n):
                random.shuffle(keywords)
                s[i] = phase1_update(source_prob, [w[1] for w in wiki_list], keywords[:k], n_iter, False, log, mode_of_operation)
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

def test_run(keywords, verbosity, log):
        '''
            Runs the complete phase 1 for a list of keywords ('keywords') on a pre-defined set of sites.
            'log' is the name of file in which log should be saved.
        '''
        if not os.path.exists(log):
                os.makedirs(log)
        logFile = open(log+'/metadata','a')
        logFile.write('Verbosity = '+ str(verbosity)+'\n')
        logFile.write('Keywords = '+ str(keywords)+'\n')
        wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com"), ("random","random")]
        logFile.write('Wiki List = '+ str(wiki_list)+'\n')
        N = len(wiki_list)
        source_prob = np.array([1.0/N for i in range(N)])
        logFile.write('Initial source probabilities = '+ str(source_prob)+'\n')
        mode_of_operation = 4
        logFile.write('Mode of operation = ' + str(mode_of_operation)+'\n')
        source_prob = phase1_update(source_prob, wiki_list, keywords, 1, verbosity, log+'/'+log, mode_of_operation)
        
        print "\n\n---------\n"
        if verbosity:
                for i in range(len(source_prob)):
                        print wiki_list[i][0], source_prob[i]/source_prob[0]
        
        #print key_wiki_err(keywords, [w[1] for w in wiki_list], 2, 3, 2, 'non_correlation_test', mode_of_operation)

if __name__ == "__main__":
        log = raw_input("Enter a name for the run : ")
        keywords = ["Delhi", "dog", "mars", "atom"]
        #keywords = ["delhi"]
        verbosity = True
        test_run(keywords, verbosity, log)
