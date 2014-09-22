import time

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests

from dgeq.models import Contribution, PartyInfo

def fetch_loc_soup(contrib):
    url = 'http://www.electionsquebec.qc.ca/applications/donateur_popup.php'
    partyinfo = PartyInfo.objects.get(party=contrib.party)
    params = {
        'idrech': contrib.contributor.dgeqid,
        'an': contrib.year,
        'fkent': partyinfo.dgeqid,
        'langue': 'fr',
    }
    r = requests.get(url, params=params)
    return BeautifulSoup(r.text)

def extract_loc(soup):
    div = soup('div', class_='affinfo')[0]
    paras = div('p')
    city = paras[1].get_text().split(':')[1].strip()
    postal_code = paras[2].get_text().split(':')[1].strip()
    if not postal_code:
        postal_code = '---'
    return city, postal_code

def parse_loc(contrib):
    soup = fetch_loc_soup(contrib)
    city, postal_code = extract_loc(soup)
    print(contrib.contributor, contrib.year, contrib.party, city, postal_code)
    contrib.city = city
    contrib.postal_code = postal_code
    contrib.save()

class Command(BaseCommand):
    args = ''
    help = 'Scrape location information from Contribution records'

    def handle(self, *args, **options):
        contribs = Contribution.objects.filter(
            postal_code='', contributor__dgeqid__isnull=False
        )
        print("%d contributions to process" % contribs.count())
        for contrib in contribs:
            parse_loc(contrib)
            time.sleep(2)

