from django.db import models
from company import Company
from company_user import CompanyUser
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User)
    company = models.ManyToManyField(Company, through='CompanyUser')
