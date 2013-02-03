from django.contrib import admin
from .models import LegislativeSession, ElectoralDivision, DeputyRole, DeputyMandate

admin.site.register(LegislativeSession)
admin.site.register(ElectoralDivision)
admin.site.register(DeputyRole)
admin.site.register(DeputyMandate)
