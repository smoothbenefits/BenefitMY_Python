from django.db import models
from user import User
from company import Company


USER_TYPE = (("Employee", "Employee"),
             ("Admin", "Admin"),
             ("Broker", "Broker"),
             ("Super", "Super"))


class CompanyUser(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    company_user_type = models.TextField(choices=USER_TYPE)

    class Meta:
        order_with_respect_to = 'company'
