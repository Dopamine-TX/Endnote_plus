#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd

prefixes="0-9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
#prefixes="A B"
filenames = [prefix + "_abrvjt.html" for prefix in prefixes.split()]

all_jnames = []
for filename in filenames:
    print("reading", filename)
    # convert html to txt
    markup_string = open(filename).read()
    txt = BeautifulSoup(markup_string, features="lxml").get_text()
    # get rid of header lines
    txtlist = txt.split("\n")[22:]

    # iter journal names 
    # for every two lines: full_name, abbr_name
    state = 1
    for line in txtlist:
        if state == 1:     # to read fullname
            assert(not line.startswith("\t"))
            fullname = line.strip()
            state = 2
        elif state == 2:   # to read abbr
            if line.startswith("\t"):
                abbr = line.strip()
                all_jnames.append((fullname, abbr))
                state = 1
            else:
                all_jnames.append((fullname, ""))
                fullname = line.strip()
                state = 2
                
        #print(fullname)
        #print(abbr)
        #print()

fullnames = [fullname for fullname, abbr in all_jnames]
abbrs = [abbr for fullname, abbr in all_jnames]

counted_fullnames = Counter(fullnames)
counted_abbrs = Counter(abbrs)
#print(len(counted_abbrs))

fullname_to_keep = set([k for k,v in counted_fullnames.items() if v == 1])
abbr_to_keep = set([k for k,v in counted_abbrs.items() if v == 1])

print("filtering")
filtered_jnames = [(fullname, abbr) for fullname, abbr in all_jnames 
    if ((fullname in fullname_to_keep) and (abbr in abbr_to_keep))]

print(len(all_jnames))
print(len(filtered_jnames))

fullnames = [fullname for fullname, abbr in filtered_jnames]
abbrs = [abbr for fullname, abbr in filtered_jnames]

df = pd.DataFrame()
df["fullnames"] = fullnames
df["abbrs"] = abbrs
print(df)
df.to_csv("jnames.csv", sep="\t", header=False, index=False)


#to_rm = [k for k,v in counted_abbrs.items() if v > 1]
#print(fullname_to_keep)

    #open(filename.split("_")[0] + ".txt", "w").write(txt)

