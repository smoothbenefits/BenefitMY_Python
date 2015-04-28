import reversion

from django.db import models
from app.custom_authentication import AuthUser
from company_fsa_plan import CompanyFsaPlan

@reversion.register
class UserCompanyFsaPlan(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_fsa_plan")
    company_life_insurance = models.ForeignKey(CompanyFsaPlan,
                                               related_name="user_company_fsa_plan")
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
