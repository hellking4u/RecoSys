# Get the first 20 hits for: "Breaking Code" WordPress blog
from google import search
x =  search('"Breaking Code" WordPress blog', stop=1)
print x.next()
