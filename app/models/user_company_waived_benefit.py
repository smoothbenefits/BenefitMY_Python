import reversion

from django.db import models
from company import Company
from benefit_type import BenefitType
from django.contrib.auth.models import User

@reversion.register
class UserCompanyWaivedBenefit(models.Model):

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    benefit_type = models.ForeignKey(BenefitType)
    reason = models.CharField(max_length=2048,
                              null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
