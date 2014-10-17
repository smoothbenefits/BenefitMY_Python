from django.db import models
from user import User
from company import Company


class Person(models.Model):
    obj_type = models.TextField(null=True)
    person_type = models.CharField(max_length=30)
    full_name = models.TextField(null=True)
    email = models.EmailField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    ssn = models.TextField(null=True)
    birth_date = models.DateField(null=True)
    user = models.ForeignKey(User, related_field = 'persons')
    company = models.ForeignKey(Company)
