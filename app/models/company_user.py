from django.db import models
from user import User
from company import Company


USER_TYPE = (("Employee", "Employee"),
             ("Admin", "Admin"),
             ("Broker", "Broker"),
             ("Super", "Super"))


class CompanyUser(models.Model):
    user_id = models.ForeignKey(User, related_name="company_user")
    company_id = models.ForeignKey(Company, related_name="company_user")
    company_user_type = models.TextField(choices=USER_TYPE)

    class Meta:
        order_with_respect_to = 'company_id'
