from django.db import models
from user import User
from company_benefit_plan_option import CompanyBenefitPlanOption


class UserCompanyBenefitPlanOption(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_benefit_plan")
    company_benefit_plan_option = models.ForeignKey(
        CompanyBenefitPlanOption,
        related_name="user_company_benefit_plan")
