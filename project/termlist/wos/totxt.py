from bs4 import BeautifulSoup

#prefixes="0-9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
prefixes="A B C D E"
filenames = [prefix + "_abrvjt.html" for prefix in prefixes.split()]

for filename in filenames:
    markup_string = open(filename).read()
    txt = BeautifulSoup(markup_string).get_text()
    txt = "\n".join(txt.split("\n")[22:])
    open(filename.split("_")[0] + ".txt", "w").write(txt)

