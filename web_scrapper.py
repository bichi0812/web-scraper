# coding: utf-8

# To getch header and contents from a website
from bs4 import BeautifulSoup
import urllib2,re, traceback, os, sys
from collections import Counter
import pandas
from sklearn.feature_extraction.text import CountVectorizer
import pymongo

url = "https://www.bing.com/search?q=custom+made+text+recognition+from+image+in+python&qs=n&form=QBRE&sp=-1&pq=custom+made+text+recognition+from+image+in+python&sc=0-49&sk=&cvid=DCB516BA224D47ADA39B27107A24F20E"
def printl(ls):
    for i in ls:
        print i
def make_matrix(headlines, vocab):
    matrix = []
    for headline in headlines:
        # Count each word in the headline, and make a dictionary.
        counter = Counter(headline)
        # Turn the dictionary into a matrix row using the vocab.
        row = [counter.get(w, 0) for w in vocab]
        matrix.append(row)
    print matrix
    df = pandas.DataFrame(matrix)
    df.columns = unique_words
    return df
def get_site_content(url):
    response = urllib2.urlopen(url)
    content = response.read()
    header = response.info()
    return [content,header]

content, header = get_site_content(url)

# implementing BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')
 # Extracting urls
links = [l.get('href') for l in soup.find_all('a') if bool(re.match(r'http.*',l.get('href'),re.I))]

# operations on text
data = soup.findAll(text=True)
print soup.text.strip()
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

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
printl(tokens)
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
# print(make_matrix(' '.join(tokens), unique_words))
def with_sklearn(tokens):
    vectorizer = CountVectorizer(lowercase=True, stop_words="english")
    matrix = vectorizer.fit_transform(tokens)
    print(matrix.todense())
# with_sklearn([" ".join(tokens)])


# In[31]:





# In[14]:


url = "https://www.bing.com/search?q=custom+made+text+recognition+from+image+in+python&qs=n&form=QBRE&sp=-1&pq=custom+made+text+recognition+from+image+in+python&sc=0-49&sk=&cvid=DCB516BA224D47ADA39B27107A24F20E"


# In[32]:


def get_site_content(url):
    response = urllib2.urlopen(url)
    content = response.read()
    header = response.info()
    return [content,header]


# In[40]:


content, header = get_site_content(url)
# implementing BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')
 # Extracting urls
links = list(set([l.get('href') for l in soup.find_all('a') if bool(re.match(r'http.*',str(l.get('href')),re.I))]))
printl(links)


# In[44]:



myclient = pymongo.MongoClient("mongodb://localhost:27017/")



# In[49]:


mydb = myclient["websites"]
print(myclient.list_database_names())


# In[50]:


mycol = mydb["urls"]


# In[52]:


print url


# In[74]:


search_engine = mydb["search_engine"]
srch_engines = [{'google':'https://www.google.com/'},{'bing':'https://www.bing.com/'}]
def process_search_engine_urls(search_engines_list):
    for rec in search_engines_list:
        for k,v in rec.items():
            try:
                search_engine.insert_one({'name':k,'url_pattern':v})
            except Exception as e:
                print traceback.exec_info()
process_search_engine_urls(srch_engines)


# In[57]:


mydb.list_collection_names()


# In[75]:


for i in mydb.search_engine.find():
    for k,v in i.items():
        print k,v


# In[82]:


search_engines = [x for x in mydb.search_engine.find()]
def process_url_with_search_engine(url,search_engines):
    s_obj = filter(lambda x:bool(re.match(x["url_pattern"],url))==True, search_engines)
    if s_obj:
        eng_name = s_obj[0]["name"]
        url_pattern = s_obj[0]["url_pattern"]
        searched_text = ""
        srch_obj = re.compile(r"(.*?=)(.*)(&qs.*)")
        if srch_obj.search(url):
            text = ' '.join(srch_obj.search(url).group(2).split('+'))
            if text:
                # add a row to db about this new query
                X = mycol.insert_one({"search_engine":eng_name,"url":url,"searched_text":text})
                if X:
                    print "record inserted !!"
process_url_with_search_engine(url, search_engines)




# In[72]:


for i in mydb.search_engine.find():
    search_engine.delete_one(i)


# In[24]:


class Url:
    def __init__(self,url):
        self.url_name = url
        self.search_engine_name = ""
        self.search_check = ""
        self.searched_text = ""
        self.contained_url = None
        self.get_details_of_url()


    def if_search_engine_used(self,url):
        search_engines = [x for x in mydb.search_engine.find()]
        s_obj = filter(lambda x:bool(re.match(x["url_pattern"],url))==True, search_engines)
        return s_obj

    def search_engine_used(self,url):
        search_engines = [x for x in mydb.search_engine.find()]
        s_obj = filter(lambda x:bool(re.match(x["url_pattern"],url))==True, search_engines)
        return s_obj

    def extract_serach_engine_name(self,url):
        if self.if_search_engine_used(url) != None:
            s_obj = if_search_engine_used(url)
            eng_name = s_obj[0]["name"]
            url_pattern = s_obj[0]["url_pattern"]
            return eng_name

    def extract_searched_text(self,url):
        searched_text = ""
        srch_obj = re.compile(r"(.*?=)(.*)(&qs.*)")
        if srch_obj.search(url):
            searched_text = ' '.join(srch_obj.search(url).group(2).split('+'))
        if searched_text:
            return searched_text

    def get_url(self):
        return self.url_name

    def get_details_of_url(self):
        url = self.get_url()
        if if_search_engine_used(url):
            self.search_check = True
            self.search_engine_name = if_search_engine_used(url)
            self.searched_text = extract_searched_text(url)



# In[90]:


url = "https://www.bing.com/search?q=custom+made+text+recognition+from+image+in+python&qs=n&form=QBRE&sp=-1&pq=custom+made+text+recognition+from+image+in+python&sc=0-49&sk=&cvid=DCB516BA224D47ADA39B27107A24F20E"
url = "https://www.google.co.in/search?q=re.findall+in+python&oq=re.findall&aqs=chrome.1.69i57j0l5.5398j0j7&sourceid=chrome&ie=UTF-8"
url = "https://developers.google.com/edu/python/regular-expressions"


# In[91]:


url


# In[92]:


content, header = get_site_content(url)
soup = BeautifulSoup(content, 'html.parser')


# In[118]:


title = soup.title.text
print title
class UrlData:
    def __init__(self,url):
        self.url_name = None
        self.title = ''
        self.content = ''
        self.links_contained = None
        self.header = None
        self.set_class_properties()


    def set_class_properties(self):
        url = self.get_url_name()
        self.content,self.header = self.get_url_content(url)
        soup = BeautifulSoup(self.content,'html.parser')
        self.title = re.sub(r"[\n\s]+","",soup.title.text)
        self.scrape_contents()

    def get_url_content(self,url):
        response = urllib2.urlopen(url)
        content = response.read()
        header = response.info()
        return [content,header]

    def get_url_name(self):
        return self.url_name
    def scrape_contents(self):
        content = self.content
        body = re.search(r"<body>.*</body>",content).group()
        if body:
            tags = list(set(re.findall(r'<\w+',content)))
            print tags


# In[120]:


# data = soup.findAll(text=True)
# def printl(ls):
#     for i in ls:
#         print i
# print ' '.join(data)
# print re.search(r"<!DOCTYPE.*<head>",content,re.M|re.I).group()
# contents = re.sub(r"[\n\s]+","",content)
# tags = list(set(re.findall(r'<\w+',content)))
# # print tags
# divs = re.findall(r"<div.*<\div>",contents)
# print divs
# print re.search(r"<head>.*</head>",contents).group()

ul = UrlData(url)



# In[47]:


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    elif re.match(r'<!.*!>', str(element.encode('utf-8'))):
        return False
    return True

result = filter(visible, data)
printl(result)
