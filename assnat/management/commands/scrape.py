from urllib.request import urlopen
import time

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from dtfapp.models import Person
from assnat.models import (LegislativeSession, ElectoralDivision, PoliticalParty, DeputyRole,
    DeputyMandate)

def fetch_soup(url):
    with urlopen(url) as fp:
        contents = fp.read()
    return BeautifulSoup(contents)

def parse_deputy(soup):
    dep_header = soup('div', class_='enteteFicheDepute')[0]
    fullname = dep_header.h1.get_text()
    lastname = dep_header.h1.span.get_text()
    firstname = fullname[:-(len(lastname)+1)]
    firstname = firstname.replace('\xa0', ' ')
    lastname = lastname.replace('\xa0', ' ')
    role_elems = dep_header.ul('li')
    roles = [elem.get_text() for elem in role_elems]
    return {
        'firstname': firstname,
        'lastname': lastname,
        'roles': roles,
    }

def extract_division(role):
    words = role.split(' ')
    print(words)
    if words[1] in {'de', 'des'}:
        return ' '.join(words[2:])
    else:
        result = ' '.join(words[1:])
        return result[2:] # Remove d'

def create_deputy_mandate(url):
    soup = fetch_soup(url)
    data = parse_deputy(soup)
    legislative_session = LegislativeSession.objects.get(legislature=40, session=1)
    person, created = Person.objects.get_or_create(firstname=data['firstname'], lastname=data['lastname'])
    print(person)
    division_name = extract_division(data['roles'][0])
    division, created = ElectoralDivision.objects.get_or_create(name=division_name)
    print('Circonscription: %s' % division)
    party, created = PoliticalParty.objects.get_or_create(name=data['roles'][1])
    print('Parti: %s' % party)
    mandate, created = DeputyMandate.objects.get_or_create(person=person, session=legislative_session)
    mandate.division = division
    mandate.party = party
    for role_name in data['roles'][2:]:
        role, created = DeputyRole.objects.get_or_create(name=role_name)
        mandate.roles.add(role)
    mandate.save()

class Command(BaseCommand):
    help = 'Scrape active deputy list from http://www.assnat.qc.ca'
    
    def handle(self, *args, **options):
        if args:
            # debug mode
            url = 'http://www.assnat.qc.ca' + args[0]
            print("Debug Scraping %s" % url)
            create_deputy_mandate(url)
            return
        
        url = 'http://www.assnat.qc.ca/fr/deputes/index.html'
        soup = fetch_soup(url)
        table = soup('table', class_='tableTriable')[0]
        rows = table.tbody('tr')
        for rowelem in rows:
            url = rowelem.td.a.attrs['href']
            print("Scraping %s" % url)
            create_deputy_mandate('http://www.assnat.qc.ca' + url)
            time.sleep(5)
