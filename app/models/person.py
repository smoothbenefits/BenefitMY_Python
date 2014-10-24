from django.db import models
from user import User
from company import Company


class Person(models.Model):
    person_type = models.CharField(max_length=30)
    full_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    ssn = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User,
                             related_name="families",
                             null=True,
                             blank=True)
    company = models.ForeignKey(Company,
                                related_name="contacts",
                                null=True,
                                blank=True)
