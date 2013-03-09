from django.shortcuts import render_to_response

from dgeq.models import Contributor
from .models import Person, Company

MAIN_MENU = [
    ('people', "Personnes"),
    ('companies', "Compagnies"),
]

def people(request):
    contributors = Contributor.contributors_by_total_amount()[:100]
    return render_to_response('people.html', {'contributors': contributors, 'menu': MAIN_MENU,
        'active_menu': 'people'})

def person_details(request, pk):
    person = Person.objects.get(id=pk)
    return render_to_response('person_details.html', {'person': person, 'menu': MAIN_MENU,
        'active_menu': 'people'})

def companies(request):
    companies = Company.objects.all()
    return render_to_response('companies.html', {'companies': companies, 'menu': MAIN_MENU,
        'active_menu': 'companies'})
