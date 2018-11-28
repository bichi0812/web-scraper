##################################################################################
##
##  Date            : 28-11-2018
##  Developed By    : Bichitra Satapathy
##
##
##################################################################################
from get_site_code import *
url = "https://thepythonguru.com/what-is-if-__name__-__main__/"

if __name__ == "__main__":
    # collect data of website whether it is active ot not
    ret_code = get_website_health(url)
    print "Site status code is "+str(ret_code)

    if ret_code == 200:
        # Get hex code of site
        the_page = get_site_content(url)
        current_hash = getHash(the_page)
        print "The hash code of current page is "+current_hash
