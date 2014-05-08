import content_extractor, TextRank, operator, os
import categorizer
import server

def doc_categorize(fsort):
    cat_prob = [0,0,0,0]
    for term in fsort:
        print term[0]
    for kw in fsort:
        term_corr = [kw[1]*term for term in categorizer.categorize(kw[0])]
        cat_prob = map(operator.add, cat_prob, term_corr)
        print 'cumulative probability :', cat_prob
    return cat_prob

def main(url, log):
    log1 = log
    while True:
        if not os.path.exists(log1):
            os.makedirs(log1)
            break
        else : log1 = log1+'_'
    content = content_extractor.get_content(url)

    logFile = open(log1+'/metadata',"a")
    logFile.write("URL : "+url+"\n\n")
    logFile.write("Title : "+content['title']+"\n\n")
    logFile.write("Meta Desc. : "+content['meta']+"\n\n")
    logFile.write("Content : "+content['content'].encode("utf8")+"\n\n")
    logFile.close()

    d = TextRank.text_rank(content['content'])
    sortd = sorted(d.iteritems(), key = operator.itemgetter(1), reverse=True)

    logtext = open(log1+'/textrank_result',"a")
    logtext.write(str(sortd))
    logtext.close()

    final=[]
    for i in sortd:
        for j in range(len(source_probs)):
            final.append((i[0], j, i[1]*source_probs[j]))

    fsort = sorted(final, key = operator.itemgetter(2), reverse=True)
    logres = open(log1+'/result',"a")
    logres.write(str(fsort))
    logres.close()
    server.run_server(fsort[:10])

if __name__ == "__main__":
    log = "client_run_tech"#raw_input("Enter a name for the run : ")
    url = 'http://www.cbsnews.com/news/astronomer-bruce-woodgate-inventor-of-the-camera-used-on-hubble-telescope-has-died/'
    main(url, log)
    #print doc_categorize(fsort[:10])