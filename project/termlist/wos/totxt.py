from bs4 import BeautifulSoup

#prefixes="0-9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
prefixes="A B"
filenames = [prefix + "_abrvjt.html" for prefix in prefixes.split()]

for filename in filenames:
    markup_string = open(filename).read()
    txt = BeautifulSoup(markup_string).get_text()
    txtlist = txt.split("\n")[22:]
    it_txtlist = iter(txtlist)
    for (fullname, abbr) in zip(it_txtlist, it_txtlist):
        fullname = fullname.strip()
        abbr = abbr.strip()
        print(fullname)
        print(abbr)
        print()

    #open(filename.split("_")[0] + ".txt", "w").write(txt)

