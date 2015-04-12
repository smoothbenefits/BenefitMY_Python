import reversion

from django.db import models
from company_benefit_plan_option import CompanyBenefitPlanOption
from user_company_waived_benefit import UserCompanyWaivedBenefit

from django.contrib.auth.models import User

@reversion.register
class UserCompanyBenefitPlanOption(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_benefit_plan")
    benefit = models.ForeignKey(
        CompanyBenefitPlanOption,
        related_name="user_company_benefit_plan")

    pcp = models.CharField(max_length=30,
                           blank=True,
                           null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
