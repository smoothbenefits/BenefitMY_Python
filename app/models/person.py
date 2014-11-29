from django.db import models
from company import Company
from django.contrib.auth.models import User
from encrypted_fields import EncryptedTextField

class Person(models.Model):
    person_type = models.CharField(max_length=30)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    ssn = EncryptedTextField(null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User,
                             related_name="family",
                             null=True,
                             blank=True)
    company = models.ForeignKey(Company,
                                related_name="contacts",
                                null=True,
                                blank=True)
