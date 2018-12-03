import urllib, urllib2, traceback, hashlib

def get_website_health(url):
    status_code = ""
    try:
        status_code = urllib.urlopen(url).getcode()
    except Exception as e:
        print "Couldn't fetch status code of the url"
        print traceback.format_exc()
    return status_code

def getHash(the_page):
    return hashlib.sha224(the_page).hexdigest()

def get_site_content(url):
    content = ""
    try:
        data = urllib2.urlopen(url)
        content = data.read()
    except Exception as e:
        print "Couldn't Fetch html content of the page"
        print traceback.format_exc()
    return content
