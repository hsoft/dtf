from urllib.request import urlopen
from urllib.parse import urlencode, urlparse, parse_qs, quote
import time
from datetime import date

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from dgeq.models import Contributor
from ...models import OIQQuery, OIQResult

def fetch_soup(url, data=None):
    if data:
        data = urlencode(data).encode('ascii')
    with urlopen(url, data) as fp:
        contents = fp.read()
    return BeautifulSoup(contents)

def parse_contact_ids(resulttable):
    result = []
    for resultrow in resulttable.tbody('tr'):
        detail_link = resultrow.td.a.attrs['href']
        qs = urlparse(detail_link).query
        contactid = parse_qs(qs)['ContactId'][0]
        result.append(contactid)
    return result

def fetch_oiq_info(query):
    firstname = query.person.firstname
    lastname = query.person.lastname
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
        print("Nothing")
        return
    contactids = parse_contact_ids(resulttable)
    print("Got %d contact ids" % len(contactids))
    for contactid in contactids:
        if OIQResult.objects.filter(contactid=contactid).exists():
            print("We've already fetched contactid %s. Skipping." % contactid)
            continue
        print("Fetching contact %s" % contactid)
        time.sleep(1)
        url = "http://www.oiq.qc.ca/fr/Pages/BottinDesMembresDetails.aspx?ContactId=" + quote(contactid)
        soup = fetch_soup(url)
        def getfield(name):
            try:
                return soup('span', id='ctl00_PlaceHolderMain_' + name)[0].get_text().strip()
            except IndexError: # It's possible that the field is not there
                return ''
        result = OIQResult(query=query)
        result.contactid = contactid
        fullname = getfield('lblContactName')
        print("The name is: %s" % fullname)
        result.lastname, result.firstname = fullname.split(', ', 1)
        result.category = getfield('lblCategory')
        result.employer = getfield('lblEmployer')
        print("Employer is: %s" % result.employer)
        result.address = getfield('lblAddress')
        result.city = getfield('lblCity')
        result.postal_code = getfield('lblPostalCode')
        result.telephone = getfield('lblPhone')
        result.graduation = getfield('lblGraduationDate')
        result.university = getfield('lblSchool')
        result.speciality = getfield('lblSpecialty')
        result.save()
        
class Command(BaseCommand):
    def handle(self, *args, **options):
        for index, contributor in enumerate(Contributor.contributors_by_total_amount()):
            print("Checking out [%d] %s (%d $)" % (index, contributor, contributor.total_amount))
            if contributor.person.oiqquery_set.count() > 0:
                print("We've already queried that person. Skipping.")
                continue
            query = OIQQuery(date=date.today(), person=contributor.person)
            query.save()
            try:
                fetch_oiq_info(query)
            except Exception:
                query.delete() # It didn't complete correctly, remove it.
            except KeyboardInterrupt:
                query.delete()
                raise
            time.sleep(1)
