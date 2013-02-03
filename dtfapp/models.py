from django.db import models

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
    
