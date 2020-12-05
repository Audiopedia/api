
import re

f = open("data.csv", 'r')
dat = f.read()
dat = re.sub("<[^>]*>", " ", dat)
f.close()

f = open("data_new.csv", 'w')
f.write(dat)
f.close()