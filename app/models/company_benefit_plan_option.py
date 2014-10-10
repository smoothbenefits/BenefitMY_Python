from django.db import models


class CompanyBenefitPlanOption(models.Model):
    total_cost_per_period = models.DecimalField()   
    employ_cost_per_period = models.DecimalField()   
    benefit_option_type = models.TextField()


    company_id = models.IntegerField()
    benefit_plan_id = models.IntegerField()
