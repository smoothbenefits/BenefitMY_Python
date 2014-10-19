from django.db import models
from person import Person


class Phone(models.Model):
    phone_type = models.CharField(max_length=10)
    number = models.CharField(max_length=32)
    person = models.ForeignKey(Person,
                               related_name='phones',
                               blank=True,
                               null=True)
