from django.contrib import admin
from .models import Contributor, Contribution, PartyInfo

class ContributorAdmin(admin.ModelAdmin):
    search_fields = ['person__lastname', 'person__firstname']
    readonly_fields = ['person']

class ContributionAdmin(admin.ModelAdmin):
    search_fields = ['contributor__person__lastname', 'contributor__person__firstname']
    list_filter = ['year', 'party']
    readonly_fields = ['contributor', 'party']

admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(PartyInfo)
