from django.db import models
from company import Company
from benefit_plan import BenefitPlan

S = ["individual",
     "individual_plus_spouse",
     "individual_plus_child",
     "individual_plus_one",
     "individual_plus_children",
     "family"]

TYPES = ([(item, item) for item in S])


class CompanyBenefitPlanOption(models.Model):
    total_cost_per_period = models.DecimalField()
    employ_cost_per_period = models.DecimalField()
    benefit_option_type = models.TextField(choices=TYPES)

    company = models.ForeignKey(Company)
    benefit_plan = models.ForeignKey(BenefitPlan)
