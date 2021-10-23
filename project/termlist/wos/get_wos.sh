letters="0-9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"

echo "$letters" | sed "s/ /\n/g" | while read l
do
    if [ -f ${l}_abrvjt.html ]; then
        echo "${l}_abrvjt.html exist"
        continue
    fi
    echo https://images.webofknowledge.com/images/help/WOS/${l}_abrvjt.html
    wget "https://images.webofknowledge.com/images/help/WOS/${l}_abrvjt.html"
done
    
