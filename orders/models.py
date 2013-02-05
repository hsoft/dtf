from django.db import models

from dtfapp.models import Person, Company

class OIQInfo(models.Model):
    person = models.ForeignKey(Person)
    contactid = models.CharField(max_length=100, unique=True)
    employer = models.ForeignKey(Company, null=True)
    employer_name = models.CharField(max_length=100)
    verification_date = models.DateField()
