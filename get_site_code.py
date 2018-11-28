import urllib, urllib2, traceback, hashlib

def get_website_health(url):
    status_code = urllib.urlopen(url).getcode()
    return status_code

def getHash(the_page):
    return hashlib.sha224(the_page).hexdigest()

def get_site_content(url):
    data = urllib2.urlopen(url)
    content = data.read()
    return content
