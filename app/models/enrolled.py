from django.db import models
from user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from person import Person


class Enrolled(models.Model):
    user_company_benefit_plan_option = models.ForeignKey(
        UserCompanyBenefitPlanOption)
    person = models.ForeignKey(Person)
