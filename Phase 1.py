__author__ = 'nikhil'
import search_module as sm
import TextRank, gurmeet
import numpy as np
verbosity = True
keyword = "Rat"

wiki_list = ["Wikipedia", "site:citizendium.org", "Britannica"]
init_prob = np.array([1.0/3 for i in range(3)])
mode_of_operation = 1
wiki_content = sm.get_wiki_article(keyword, verbose=verbosity, search_list=wiki_list)

print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
[source_prob, sorted_list] = gurmeet.tfidf(init_prob, wiki_content[0], wiki_content[1], wiki_content[2], mode_of_operation=mode_of_operation, return_term=0)
#tr_list = TextRank.text_rank(wiki_content[0])

print "The top 15 keywords :"
for g, v in sorted_list[:15]:
    print g, v,
    print '\t',
print "---------"
for i in range(len(source_prob)):
	print wiki_list[i], source_prob[i]/source_prob[0]
