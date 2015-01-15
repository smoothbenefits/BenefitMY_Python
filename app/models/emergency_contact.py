from person import Person
from django.db import models


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    person = models.ForeignKey(Person,
                               related_name='ec',
                               blank=True,
                               null=True)
