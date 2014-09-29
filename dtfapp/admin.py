from django.contrib import admin
from .models import Person, Company, PoliticalParty, EmploymentRole, Employment

admin.site.register(Person)
admin.site.register(Company)
admin.site.register(PoliticalParty)
admin.site.register(EmploymentRole)
admin.site.register(Employment)

