from django.contrib import admin
from .models import OIQQuery, OIQResult

admin.site.register(OIQQuery)
admin.site.register(OIQResult)
