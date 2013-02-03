from django.contrib import admin
from .models import LegislativeSession, ElectoralDivision, PoliticalParty, DeputyRole, DeputyMandate

admin.site.register(LegislativeSession)
admin.site.register(ElectoralDivision)
admin.site.register(PoliticalParty)
admin.site.register(DeputyRole)
admin.site.register(DeputyMandate)
