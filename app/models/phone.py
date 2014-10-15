from django.db import models
from person import Person


class Phone(models.Model):
    phone_type = models.TextField()
    number = models.TextField()
    person = models.ForeignKey(Person, related_name='phones')
    

