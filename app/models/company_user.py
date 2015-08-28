import reversion

from django.db import models
from company import Company
from app.custom_authentication import AuthUser

USER_TYPE_EMPLOYEE = "employee"
USER_TYPE_ADMIN = "admin"
USER_TYPE_BROKER = "broker"
USER_TYPE_SUPER = "super"
USER_TYPE = ((USER_TYPE_EMPLOYEE, "employee"),
             (USER_TYPE_ADMIN, "admin"),
             (USER_TYPE_BROKER, "broker"),
             (USER_TYPE_SUPER, "super"))

@reversion.register
class CompanyUser(models.Model):
    user = models.ForeignKey(AuthUser)
    company = models.ForeignKey(Company)
    company_user_type = models.TextField(choices=USER_TYPE)
    new_employee = models.BooleanField(default=True)
