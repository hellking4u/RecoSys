__author__ = 'nikhil'
import search_module as sm
import TextRank, gurmeet

verbosity = True
keyword = "Britain"

mode_of_operation = 1
wiki_content = sm.get_wiki_article(keyword, verbose=verbosity)

print "\n\n Done with Content Extraction. Begin keyword extraction algorithm..."
tr_list = gurmeet.tfidf(wiki_content[0], wiki_content[1], wiki_content[2], mode_of_operation=mode_of_operation, return_term=0)
#tr_list = TextRank.text_rank(wiki_content[0])

for g, v in tr_list:
    print g, v