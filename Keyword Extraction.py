__author__ = 'nikhil'
import tfidf
import TextRank, gurmeet


ltf = gurmeet.test_corpus_probs_update(["test_corpus_file_1.txt", "test_corpus_file_2.txt","test_corpus_file_3.txt"], mode_of_operation = 2, return_term=0)
atf = gurmeet.test_corpus_probs_update(["test_corpus_file_1.txt", "test_corpus_file_2.txt","test_corpus_file_3.txt"], mode_of_operation = 3, return_term=0)
text = open("test_corpus_file_1.txt").read()
tr_list = TextRank.text_rank(text)
print ltf
print atf
print tr_list

#---- Imported TextRank module ----#

#
#print(tr_list)
#for k,g in tr_list:
#    print k,g
