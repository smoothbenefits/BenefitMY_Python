import reversion

from django.db import models
from company import Company
from django.conf import settings

USER_TYPE = (("employee", "employee"),
             ("admin", "admin"),
             ("broker", "broker"),
             ("super", "super"))

@reversion.register
class CompanyUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey(Company)
    company_user_type = models.TextField(choices=USER_TYPE)
    new_employee = models.BooleanField(default=True)
