from urllib.request import urlopen, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode

from bs4 import BeautifulSoup

def fetch_soup(url, data=None, withdesturl=False, cookiejar=None):
    if data:
        data = urlencode(data).encode('ascii')
    if cookiejar:
        myopen = build_opener(HTTPCookieProcessor(cookiejar)).open
    else:
        myopen = urlopen
    with myopen(url, data) as fp:
        desturl = fp.geturl()
        contents = fp.read()
    if withdesturl:
        return BeautifulSoup(contents), desturl
    else:
        return BeautifulSoup(contents)
