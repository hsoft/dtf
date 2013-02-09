from django.db import models

from dtfapp.models import Person

class OIQQuery(models.Model):
    date = models.DateField(db_index=True)
    person = models.ForeignKey(Person)
    
    def __str__(self):
        return "%s (%s)" % (self.person, self.date)

class OIQResult(models.Model):
    query = models.ForeignKey(OIQQuery)
    contactid = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100, db_index=True)
    lastname = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    graduation = models.CharField(max_length=20)
    university = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    
    def __str__(self):
        return "%s, %s [%s]" % (self.lastname, self.firstname, self.employer)
