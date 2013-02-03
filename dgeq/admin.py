from django.contrib import admin
from .models import Contributor, Contribution, PartyInfo

admin.site.register(Contributor)
admin.site.register(Contribution)
admin.site.register(PartyInfo)
