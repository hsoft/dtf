from urllib.parse import urlparse, parse_qs
from http.cookiejar import CookieJar
import time
from datetime import date

from django.core.management.base import BaseCommand

from urllib.request import urlopen, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

# NOTE: This script doesn't work. At all.

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

def test():
    url = 'http://www.registreentreprises.gouv.qc.ca/aa__scripts/services.aspx?serv=S00436&langue=F'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    form = soup('form')[0]
    hidden_inputs = form('input', type='hidden')
    post_data = {}
    for input in hidden_inputs:
        post_data[input.attrs['name']] = input.attrs['value']
    post_data['ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$K1Fieldset1$ChampRecherche$_cs'] = 'SNC Lavallin'
    # post_data['__VIEWSTATE'] = '/wEPDwUENTM4MQ9kFgJmD2QWBgIBDxYCHgRUZXh0BRd4bWw6bGFuZz0iZnIiIGxhbmc9ImZyImQCAw9kFgICAQ8WAh8ABZEDDQo8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Ii9LMVJlc3NvdXJjZXMvRmV1aWxsZVN0eWxlL2ltcG9ydEdSLmNzcyIgdHlwZT0idGV4dC9jc3MiIC8+DQoNCjxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iL0sxUmVzc291cmNlcy9GZXVpbGxlU3R5bGUvQmFuZGVhdUdSLmNzcyIgdHlwZT0idGV4dC9jc3MiIC8+DQoNCjwhLS1baWYgbHRlIElFIDZdPg0KPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSIvSzFSZXNzb3VyY2VzL0ZldWlsbGVTdHlsZS9pZS1vbmx5LmNzcyIgdHlwZT0idGV4dC9jc3MiIC8+DQoNCjwhW2VuZGlmXS0tPg0KPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSIvSzFSZXNzb3VyY2VzL0ZldWlsbGVTdHlsZS9iaWRvbi5jc3MiIHR5cGU9InRleHQvY3NzIiAvPg0KDQpkAgUPZBYIAgMPZBYCZg9kFgRmD2QWAmYPDxYCHghJbWFnZVVybAUgL0sxUmVzc291cmNlcy9JbWFnZXMvMzAxNTZfMS5naWYWAh4DYWx0BSZSZWdpc3RyYWlyZSBkZXMgZW50cmVwcmlzZXMgZHUgUXXDqWJlY2QCAQ9kFgJmD2QWAmYPDxYEHwAFQUZlcm1lciBsYSBzZXNzaW9uIDxpbWcgc3JjPSIvSzFSZXNzb3VyY2VzL0ltYWdlcy8yMzc1Nl8xX2YuZ2lmIiA+HgdUb29sVGlwBRFGZXJtZXIgbGEgc2Vzc2lvbmRkAhEPZBYCAgEPZBYCAgEPDxYCHwEFIC9LMVJlc3NvdXJjZXMvSW1hZ2VzLzIzNzY0XzEuZ2lmFgIfAgUQSW1wcmltZXIgbGEgcGFnZWQCHw9kFgICAQ9kFgJmD2QWBGYPDxYGHghDc3NDbGFzcwUQY2hhbXBvYmxpZ2F0b2lyZR4EXyFTQgICHgdWaXNpYmxlaGRkAgEPZBYCZg9kFgYCBA9kFgICAQ9kFgICAQ9kFgYCAg9kFgJmDw8WCB4JRm9yZUNvbG9yDB4HRGlzcGxheQsqKlN5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuVmFsaWRhdG9yRGlzcGxheQIeDEVycm9yTWVzc2FnZQVXTGEgcmVjaGVyY2hlIG5lIHBldXQgw6p0cmUgbGFuY8OpZSBzaSBsYSB6b25lIGRlIHRleHRlIGVzdCB2aWRlLjxzcGFuPiAoMzE0MjYpIDwvc3Bhbj4gHwUCBGRkAgUPFgIfBmhkAgoPDxYIHglNYXhMZW5ndGgC+gEeBVdpZHRoGwAAAAAAwIJAAQAAAB4ETW9kZQsqJVN5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuVGV4dEJveE1vZGUAHwUCgAIWAh4FdGl0bGUFA05vbWQCBg8WAh4cS1JCVFJlY2hTaW1wbGVfUmVjaGVyY2hlcl9jdmhkAggPDxYEHwAFElJlY2hlcmNoZSBhdmFuY8OpZR8DBRJSZWNoZXJjaGUgYXZhbmPDqWVkZAIlD2QWAgIBD2QWAgIODw8WAh8BBSAvSzFSZXNzb3VyY2VzL0ltYWdlcy8yMzMzOF8xLmdpZhYCHwIFIlBvcnRhaWwgZHUgZ291dmVybmVtZW50IGR1IFF1w6liZWNkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBVFjdGwwMCRDUEhfSzFab25lQ29udGVudTFfQ2FkciRJZFNlY3Rpb25SZWNoU2ltcGxlJElkU2VjdGlvblJlY2hTaW1wbGUkSzFGaWVsZHNldDGJ48WEt02l+QsfmlI0VlKlUEwn7Q=='
    # post_data['__EVENTVALIDATION'] = '/wEWBgK0obWeCgL0mNkcAtLTz5oEAvjC1ZYBAsbRkbgPApPJ0JoDadfjeB9z75yPuNEO6VT5Nh0WoLQ='
    print(r.url)
    cookies = r.cookies
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0',
        'Referer': 'https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436&Clng=F',
        'Host': 'www.registreentreprises.gouv.qc.ca',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    # cookies = {
    #     'LGSIEET1Utilisateur': 'Key',
    #     'LGSIEET1JETON': 'IDUTL',
    #     'LGSIEE': 'Cusr',
    #     'K1LNG': 'F',
    #     'EtatCadri-S00436-lvx5uxgvtmj5ommvmokzum1l': 'PABDAG8AbgB0AGUAbgBlAHUAcgBPAGIAagBlAHQARQB0AGEAdAA+AA0ACgAgACAAPABFAHQAYQB0AEEAZgBmAGkAYwBoAGEAZwBlAD4ADQAKACAAIAAgACAAPABQAGEAZwBlAEMAbwB1AHIAYQBuAHQAZQA+AEkAZABQAGEAZwBlAFIAZQBjAGgAUwBpAG0AcABsAGUAPAAvAFAAYQBnAGUAQwBvAHUAcgBhAG4AdABlAD4ADQAKACAAIAAgACAAPABVAHIAbABDAG8AdQByAGEAbgB0ACAALwA+AA0ACgAgACAAIAAgADwARABpAGEAbABvAGcAdQBlAEEAYwB0AGkAZgA+AEYAYQBsAHMAZQA8AC8ARABpAGEAbABvAGcAdQBlAEEAYwB0AGkAZgA+AA0ACgAgACAAIAAgADwASQBkAEQAaQBhAGwAbwBnAHUAZQAgAC8APgANAAoAIAAgACAAIAA8AEMAbwBuAGYAaQByAG0AZQBBAGMAdABpAGYAPgBGAGEAbABzAGUAPAAvAEMAbwBuAGYAaQByAG0AZQBBAGMAdABpAGYAPgANAAoAIAAgACAAIAA8AEkAZABDAG8AbgBmAGkAcgBtAGUAIAAvAD4ADQAKACAAIAA8AC8ARQB0AGEAdABBAGYAZgBpAGMAaABhAGcAZQA+AA0ACgA8AC8AQwBvAG4AdABlAG4AZQB1AHIATwBiAGoAZQB0AEUAdABhAHQAPgA',
    #     'ASP.NET_SessionId': 'lvx5uxgvtmj5ommvmokzum1l',
    # }
    time.sleep(5)
    foo = requests.post(r.url, data=post_data, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.text)
    import pdb; pdb.set_trace()
    return soup

class Command(BaseCommand):
    def handle(self, *args, **options):
        soup = test()
        import pdb; pdb.set_trace()
