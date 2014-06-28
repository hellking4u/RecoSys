from globalsfile import *

x = load_cache()
print x.keys()
for key in x.keys():
	print key, x[key][:50].encode("utf8")