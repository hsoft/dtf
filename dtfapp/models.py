import unicodedata

from django.db import models
from django.core.urlresolvers import reverse

# Of course, we can have more than one person with the same name, but, at least at this stage of
# development, we'll act as if names were unique. Will it lead to multiple people sharing the same
# name? Of course. But since I'm not sure how to handle the problem yet, we'll fix that later.
class Person(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    class Meta:
        unique_together = (('lastname', 'firstname'),)

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)

    def get_absolute_url(self):
        return reverse('person_details', args=[str(self.id)])

    def normalized_name(self):
        # Removes all accents and then lowercase the thing, then returns
        # "lastname, firstname"
        def deaccent_char(c):
            decomposed = unicodedata.decomposition(c)
            if decomposed:
                basechar = int(decomposed.split(' ')[0], 16)
                return chr(basechar)
            else:
                return c

        result = '{}, {}'.format(self.lastname, self.firstname)
        result = ''.join(deaccent_char(c) for c in result)
        return result.lower()


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PoliticalParty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class EmploymentRole(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

class Employment(models.Model):
    employee = models.ForeignKey(Person)
    employer = models.ForeignKey(Company)
    # The date at which our source data was queried. We used to have start/end dates in this model
    # but since we didn't have a dataset giving us this information yet, I scrapped them.
    query_date = models.DateField(null=True, blank=True)
    role = models.ForeignKey(EmploymentRole)
