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
    company_user_type = models.TextField(choices=USER_TYPE, db_index=True)
    new_employee = models.BooleanField(default=True)

    def __str__(self):
        user_str = str(self.user.id)
        if (self.user.first_name and self.user.last_name):
            user_str = self.user.first_name + ' ' + self.user.last_name
        
        company_str = str(self.company.id)
        if (self.company.name):
            company_str = self.company.name

        return '{0} [{1}]'.format(user_str, company_str)
