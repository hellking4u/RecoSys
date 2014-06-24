"""
Main module form the phase 1 of the project.

Functions :
phase1_update
key_wiki_err
test_run
"""

import utilities
import numpy as np
import random, math
import os
import search_module as sm
import globalsfile as gl

def phase1_update(cat , keywords, n_iter = 1, verbosity = False, lambd = 0, log = None, mode_of_operation = 5, run_mean_mode = True):
        '''
            Compute and return the updated source priorities based on the initial priorities (gl.source_probs) and the keywords.
            Can use text rank (default) as well as tf-idf to do so.
            'log' is the name of file in which log should be saved.
        '''
        j=0

        if not log == None:
                logFile = open(log+'_intermediate_probs',"a")

        for kw in keywords:
                j = j+1
                gl.count[cat] = gl.count[cat] + 1
                wiki_content = sm.get_wiki_article(kw, verbose=verbosity, search_list=[w[1] for w in gl.cat_list[cat]])  #Get the content of the web pages respected to each website for the keyword 'kw'

                if not log == None:
                        logwiki = open(log+"_"+kw+"_wiki_contents","a")
                        for n in range(len(wiki_content)):
                                logwiki.write(gl.cat_list[cat][n][0]+' :\n')
                                logwiki.write(wiki_content[n].encode("utf8")+'\n\n\n')
                        logwiki.close()

                if verbosity : print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."

                if log == None:
                        log1 = None
                else :
                        log1 = log+'_'+str(j)+'_'+kw

                if run_mean_mode == False:
                        lambd1 = lambd
                else:
                        lambd1 = gl.count[cat]/(gl.count[cat] + 1.0)

                if mode_of_operation == 4:
                        gl.source_probs[cat] = utilities.textrank(gl.source_probs[cat], wiki_content, lambd = lambd1, log = log1)
                elif mode_of_operation == 5:
                        gl.source_probs[cat] = utilities.rake(gl.source_probs[cat], wiki_content, lambd = lambd1, log = log1)     
                else:
                        gl.source_probs[cat] = utilities.tfidf(gl.source_probs[cat], wiki_content, lambd = lambd1, log = log1, mode_of_operation=mode_of_operation, return_term=0)
                
                if verbosity : print "\n\n---------\n"

                for i in range(len(gl.source_probs[cat])):
                        if verbosity : print gl.cat_list[cat][i][0], gl.source_probs[cat][i]/gl.source_probs[cat][0]
                        if not log == None: logFile.write(gl.cat_list[cat][i][0]+" : "+str(gl.source_probs[cat][i])+'\t')
                logFile.write('\n')

        if not log == None:
                logFile.close()
                logoutput = open(log,"a")
                logoutput.write("Source Probs : "+ str(gl.source_probs[cat])+'\n')
                logoutput.close()

        #tr_list = TextRank.text_rank(wiki_content[0])
        return gl.source_probs[cat]

def key_wiki_err(keywords, wiki_list, k, n, n_iter = 1, log = None, mode_of_operation = 4):
        '''
            Compute and return the non-correlation between sites and the keywords.
            'log' is the name of file in which log should be saved.
        '''
        N = len(wiki_list)
        gl.source_probs = np.array([1.0/N for i in range(N)])
        s = np.empty((n, N))

        for i in range(n):
                random.shuffle(keywords)
                s[i] = phase1_update(gl.source_probs, [w[1] for w in wiki_list], keywords[:k], n_iter = n_iter, verbosity = False, log = log, mode_of_operation = mode_of_operation)

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

def test_run(keywords, verbosity = False, lambd = 0, log = None):
        '''
            Runs the complete phase 1 for a list of keywords ('keywords') on a pre-defined set of sites.
            'log' is the name of file in which log should be saved.
        '''
        if not log == None:
                if not os.path.exists(log):
                        os.makedirs(log)
                logFile = open(log+'/metadata','a')
                logFile.write('Verbosity = '+ str(verbosity)+'\n')
                logFile.write('Keywords = '+ str(keywords)+'\n')

        mode_of_operation = 5
        
        if not log == None:
                logFile.write('Wiki List = '+ str(gl.cat_list['general'])+'\n')
                logFile.write('Initial source probabilities = '+ str(gl.source_probs['general'])+'\n')
                logFile.write('Mode of operation = ' + str(mode_of_operation)+'\n')
                gl.source_probs = phase1_update('general', keywords, 1, verbosity, lambd = lambd, log = log+'/'+log, mode_of_operation = mode_of_operation)
        else:
                gl.source_probs = phase1_update('general', keywords, 1, verbosity, lambd = lambd, log = None, mode_of_operation = mode_of_operation)

        print "\n\n---------\n"

        if verbosity:
                for i in range(len(gl.source_probs)):
                        print gl.cat_list['general'][i][0], gl.source_probs[i]/gl.source_probs[0]
        
        #print key_wiki_err(keywords, [w[1] for w in wiki_list], 2, 3, 2, 'non_correlation_test', mode_of_operation)

if __name__ == "__main__":
        """
                A Test for the module.
        """
        
        gl.init()
        log_name = "Second_test_RAKE"
        #raw_input("Enter a name for the run : ")
        #keywords = ["Delhi", "dog", "mars", "atom"]
        keywords = ["India", "dog", "metabolism", "atom", "Biology","United States of America", "Led Zeppelin", "Prime number"]
        test_run(keywords, verbosity = True, lambd = 0.7, log = log_name)
