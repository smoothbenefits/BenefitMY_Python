from django.db import models
from company import Company
from benefit_plan import BenefitPlan

class CompanyBenefitPlanOption(models.Model):
    total_cost_per_period = models.DecimalField()
    employ_cost_per_period = models.DecimalField()
    benefit_option_type = models.TextField()

    company = models.ForeignKey(Company)
    benefit_plan = models.ForeignKey(BenefitPlan)
