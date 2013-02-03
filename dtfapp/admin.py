from django.contrib import admin
from .models import Person, Company, PoliticalParty

admin.site.register(Person)
admin.site.register(Company)
admin.site.register(PoliticalParty)
