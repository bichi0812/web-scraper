##################################################################################
##
##  Date            : 28-11-2018
##  Developed By    : Bichitra Satapathy
##
##
##################################################################################
from get_site_code import *
from bs4 import BeautifulSoup
import pandas
import re


url = "https://thepythonguru.com/what-is-if-__name__-__main__/"


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

if __name__ == "__main__":
    # collect data of website whether it is active ot not
    ret_code = get_website_health(url)
    print "Site status code is "+str(ret_code)

    if ret_code == 200:
        # Get hex code of site
        the_page = get_site_content(url)
        current_hash = getHash(the_page)
        print "The hash code of current page is "+current_hash

        # we will try to play with html contents of the web page
        # 1. We will strip all the tags and fetch the wordcount
        # For this purpose we will use BeautifulSoup to extract only text

        # implementing BeautifulSoup
        soup = BeautifulSoup(the_page, 'html.parser')

        # Extracting all possible urls
        links = [l.get('href') for l in soup.find_all('a') if bool(re.match(r'http.*',l.get('href'),re.I))]

        # operations on text
        data = soup.findAll(text=True)
        print soup.text.strip()


        result = filter(visible, data)

        # print result
        tokens = [re.sub(r'(.*)(\n+)',r'\1',x) for x in result]
        tokens = [y.strip() for y in tokens if y.encode('utf-8') not in ['\n','']]

        # filtering the urls
        tokens = [y for y in tokens if bool(re.search(r'.*http.*',y)) == False]
        # Lowercase, then replace any non-letter, space, or digit character in the headlines.
        tokens = [re.sub(r'[^\w\s\d]','',h.lower()) for h in tokens]
        # Replace sequences of whitespace with a space character.
        tokens = [re.sub("\s+", " ", h) for h in tokens]

        tokens = [x for x in tokens if x not in ['','\n']]
        unique_words = list(set(" ".join(tokens).split(" ")))
        print tokens
        # We've reduced the number of columns in the matrix a bit.
        # print(make_matrix(' '.join(tokens), unique_words))
        # print tokens
        # Read in and split the stopwords file.
        with open("stop_words.txt", 'r') as f:
            stopwords = f.read().split("\n")

        # Do the same punctuation replacement that we did for the headlines,
        # so we're comparing the right things.
        stopwords = [re.sub(r'[^\w\s\d]','',s.lower()) for s in stopwords]

        # Remove stopwords from the vocabulary.
        unique_words = [w for w in unique_words if w not in stopwords]
        print unique_words


        # # print(make_matrix(' '.join(tokens), unique_words))
        # def with_sklearn(tokens):
        #     vectorizer = CountVectorizer(lowercase=True, stop_words="english")
        #     matrix = vectorizer.fit_transform(tokens)
        #     print(matrix.todense())
        # with_sklearn([" ".join(tokens)])

        # we will try to count number of words and put in pandas

        # key will the word and value will be the count of that word
        word_count_dict = {x:len(re.findall(x,the_page)) for x in set(unique_words)}

        print word_count_dict
