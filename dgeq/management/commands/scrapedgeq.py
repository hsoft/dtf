from urllib.parse import urlparse, parse_qs
import time

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests

from dtfapp.models import Person, PoliticalParty
from dgeq.models import Contributor, Contribution

def fetch_contriblist_soup(year, page):
    url = 'http://www.electionsquebec.qc.ca/francais/provincial/financement-et-depenses-electorales/recherche-sur-les-donateurs.php'
    # PLQ, PQ, CAQ, ADQ, ON, QS
    parties = '00085|00083|00016|00065|00010|00049'
    data = [
        ('control_1[]', [str(year)]),
        ('control_2[]', parties.split('|')),
        ('control_5[]', '1|2|3|4'.split('|')),
        ('nom', ''),
        ('ckparti', 'on'),
        ('somme_minimum', '50'),
        ('somme_maximum', '3000'),
        ('liste_tri', 'NOM_PRENOM_DONATEUR'),
        ('action', 'resultat'),
    ]
    r = requests.post(url, params={'page': page}, data=data)
    return BeautifulSoup(r.text)

PARTY_NAME_REL = {
    'P.L.Q./Q.L.P.': 'PLQ',
    'Q.S.': 'QS',
    'C.A.Q.- É.F.L.': 'CAQ',
    'P.Q.': 'PQ',
    'A.D.Q.': 'ADQ',
    'O.N.': 'ON',
}
def extract_contributions(soup):
    table = soup('table', class_='tableau')[0]
    rows = table('tr')[1:-1] # first row is header and last row is a footer
    for row_elem in rows:
        cells = row_elem('td')
        if cells[0].a:
            # We have a contributor URL (and thus ID)
            url = cells[0].a.attrs['href']
            qs = urlparse(url).query
            contribid = parse_qs(qs)['idrech'][0]
            fullname = cells[0].a.get_text()
        else:
            # We only have the name
            fullname = cells[0].get_text()
            contribid = None
        lastname, firstname = fullname.strip().split(', ', 1)
        amount = cells[1].get_text()
        # The amount looks like '3 000,00 $' and we remove the ',00 $' part.
        amount = int(amount.strip().replace('\xa0', '')[:-5])
        try:
            count = int(cells[2].get_text())
        except ValueError: # n/d
            count = 1
        partyacronym = PARTY_NAME_REL[cells[3].get_text()]
        yield contribid, lastname, firstname, partyacronym, amount, count

def parse_contributions(year, page):
    soup = fetch_contriblist_soup(year, page)
    for contribid, lastname, firstname, partyacronym, amount, count in extract_contributions(soup):
        print('Processing ', contribid, lastname, firstname, partyacronym, amount, count)
        person, created = Person.objects.get_or_create(firstname=firstname, lastname=lastname)
        contribid = int(contribid) if contribid else None
        contributor, created = Contributor.objects.get_or_create(dgeqid=contribid, person=person)
        party = PoliticalParty.objects.get(acronym=partyacronym)
        contribution, created = Contribution.objects.get_or_create(
            contributor=contributor, party=party, year=year
        )
        contribution.count = count
        contribution.amount = amount
        contribution.save()
    return soup


class Command(BaseCommand):
    args = 'year <frompage>'
    help = 'Scrape contributions to party'

    def handle(self, *args, **options):
        year = args[0]
        if len(args) == 2:
            page = int(args[1])
        else:
            page = 1
        while True:
            print("Processing page %d" % page)
            soup = parse_contributions(year, page)
            time.sleep(5)
            # To know if we're on the last page, we look for the existence of the "Fin" link, which
            # is in the 4th TD of the 1st row of the last table
            if not soup('table')[-1].tr('td')[3].a:
                print("Last page reached")
                break
            page += 1
