from urllib.request import urlopen
from urllib.parse import urlencode, urlparse, parse_qs
import time
from datetime import date

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from bs4 import BeautifulSoup

from dtfapp.models import Company
from dgeq.models import Contributor
from ...models import OIQInfo

def fetch_soup(url, data=None):
    if data:
        data = urlencode(data).encode('ascii')
    with urlopen(url, data) as fp:
        contents = fp.read()
    return BeautifulSoup(contents)

def find_name_in_result_table(firstname, lastname, resulttable):
    for resultrow in resulttable.tbody('tr'):
        found_firstname = resulttable.tbody.tr('td')[1].get_text().strip()
        found_lastname = resulttable.tbody.tr.td.a.get_text().strip()
        if (found_lastname == lastname) or (found_firstname == firstname):
            return resultrow
    return None

def fetch_oiq_info(firstname, lastname):
    url = 'http://www.oiq.qc.ca/fr/Pages/BottinDesMembres.aspx'
    soup = fetch_soup(url)
    hidden_inputs = soup('form', {'name':'aspnetForm'})[0]('input', type='hidden')
    post_data = {}
    for input in hidden_inputs:
        post_data[input.attrs['name']] = input.attrs['value']
    post_data['ctl00$PlaceHolderMain$txtLName'] = lastname
    post_data['ctl00$PlaceHolderMain$txtFName'] = firstname
    soup = fetch_soup(url, post_data)
    resulttable = soup('table', id='ctl00_PlaceHolderMain_tblResults')[0]
    if resulttable.tbody is None: # no result
        return None
    resultrow = find_name_in_result_table(firstname, lastname, resulttable)
    if resultrow is None:
        print("Got a result table, but could find the correct name in the %d rows" % len(resulttable.tbody('tr')))
        return None
    detail_link = resultrow.td.a.attrs['href']
    qs = urlparse(detail_link).query
    contactid = parse_qs(qs)['ContactId'][0]
    detail_url = 'http://www.oiq.qc.ca/fr/Pages/' + detail_link
    soup = fetch_soup(detail_url)
    employer = soup('span', id='ctl00_PlaceHolderMain_lblEmployer')[0].get_text().strip()
    return (contactid, employer)
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        for index, contributor in enumerate(Contributor.contributors_by_total_amount()):
            if index < 909:
                continue
            print("Checking out [%d] %s (%d $)" % (index, contributor, contributor.total_amount))
            if contributor.person.oiqinfo_set.count() > 0:
                print("Oh well, after all no because we already have info on that person.")
                continue
            info = fetch_oiq_info(contributor.person.firstname, contributor.person.lastname)
            if info is None:
                print("Nothing")
                continue
            else:
                contactid, employer = info
                print("Got it! Employer is %s" % employer)
                try:
                    info, created = OIQInfo.objects.get_or_create(contactid=contactid, person=contributor.person)
                except IntegrityError:
                    print("We've already entered the same contact ID! Well, skipping")
                    continue
                info.verification_date = date.today()
                if employer:
                    info.employer_name = employer
                    info.employer, created = Company.objects.get_or_create(name=employer)
                    info.save()
            time.sleep(5)
