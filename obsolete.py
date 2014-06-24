import re

def words_dict(s):
    d = {}
    for i in re.findall("[a-zA-Z']+",s):
        temp = i.lower()
        if d.has_key(temp) : d[temp] = d[temp] + 1
        else : d[temp] = 1
    return d

def sorted_words_rf(d):
    return sorted(d.items(), key = lambda x: x[1], reverse = True)

def test_words_rf():
    f = open("dog.txt","r")
    d = sorted_words_rf(words_dict(f.read()))
    print d[:100]
    f.close()
