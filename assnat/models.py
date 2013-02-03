from django.db import models

from dtfapp.models import Person

class LegislativeSession(models.Model):
    legislature = models.IntegerField()
    session = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = (('legislature', 'session'), )
    
    def __str__(self):
        return "Legislature: %d Session: %d" % (self.legislature, self.session)

class ElectoralDivision(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name

class PoliticalParty(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name

class DeputyRole(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
        return self.name

class DeputyMandate(models.Model):
    session = models.ForeignKey(LegislativeSession)
    person = models.ForeignKey(Person)
    division = models.ForeignKey(ElectoralDivision, null=True)
    party = models.ForeignKey(PoliticalParty, null=True)
    roles = models.ManyToManyField(DeputyRole)
    
    class Meta:
        unique_together = (
            ('session', 'division'),
            ('session', 'person'),
        )
    
    def __str__(self):
        return str(self.person)
