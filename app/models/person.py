from django.db import models
from address import Address
from phone import Phone


class Person(models.Model):
    obj_id = models.IntegerField()
    obj_type = models.TextField()    
    person_type = models.CharField(max_length=30) 
    full_name = models.TextField()
    email = models.TextField()
    relationship = models.CharField(max_length=30, blank=True)
    ssn = models.TextField()
    birth_date = models.DateField()
    addresses = models.ForeignKey(Address)
    phones = models.ForeignKey(Phone)

    class Meta:
        app_label = 'app'
