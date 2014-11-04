from django.db import models
from company import Company
from django.contrib.auth.models import User

USER_TYPE = (("Employee", "Employee"),
             ("Admin", "Admin"),
             ("Broker", "Broker"),
             ("Super", "Super"))


class CompanyUser(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    company_user_type = models.TextField(choices=USER_TYPE)

