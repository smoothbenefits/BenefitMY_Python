from django.db import models


class UserCompanyBenefitPlanOption(models.Model):

    user_id = models.IntegerField()
    company_benefit_plan_option_id = models.IntegerField()
