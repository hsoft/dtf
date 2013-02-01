from django.shortcuts import render_to_response

from .models import Person, Company

MAIN_MENU = [
    ('people', "Personnes"),
    ('companies', "Compagnies"),
]

def people(request):
    people = Person.objects.all()
    return render_to_response('people.html', {'people': people, 'menu': MAIN_MENU,
        'active_menu': 'people'})

def companies(request):
    companies = Company.objects.all()
    return render_to_response('companies.html', {'companies': companies, 'menu': MAIN_MENU,
        'active_menu': 'companies'})
