from django.db import models
from address import Address
from phone import Phone


class Person(models.Model):
    person_type = models.CharField(max_length=30)
    relationship = models.CharField(max_length=30, blank=True)
    addresses = model.ForeignKey(Address)
    phones = model.ForeignKey(Phone)

    class Meta:
        app_label = 'app'
