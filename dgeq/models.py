from django.db import models

from dtfapp.models import Person, PoliticalParty

class Contributor(models.Model):
    person = models.ForeignKey(Person)
    # In DGEQ's contribution list, there's this "idrech" value which seems to be a unique id for
    # each contributor. We can use this ID for further queries.
    dgeqid = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.person)

class Contribution(models.Model):
    contributor = models.ForeignKey(Contributor)
    party = models.ForeignKey(PoliticalParty)
    year = models.IntegerField()
    # The number of payment that the amount was spanned in over the year. Not very useful, but since
    # we have the information, why not keep it?
    count = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    
    class Meta:
        unique_together = (
            ('contributor', 'party', 'year'),
        )
    
    def __str__(self):
        return "[%s] %s --> %s (%s)" % (self.year, self.contributor.person, self.party.acronym, self.amount)

# Extra party info related to DGEQ
class PartyInfo(models.Model):
    party = models.OneToOneField(PoliticalParty)
    dgeqid = models.CharField(max_length=16)
