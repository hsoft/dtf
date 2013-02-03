from django.db import models

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
    

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    

class PoliticalParty(models.Model):
    name = models.CharField(max_length=64, unique=True)
    acronym = models.CharField(max_length=8, unique=True)
    
    def __str__(self):
        return self.name
