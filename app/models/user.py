from django.db import models
from company import Company
from company_user import CompanyUser


class User(models.Model):
    full_name = models.TextField()
    email = models.EmailField(max_length=255)
    encrypted_password = models.TextField(null=True)
    tz = models.TextField(null=True)
    company = models.ManyToManyField(Company, through='CompanyUser')
