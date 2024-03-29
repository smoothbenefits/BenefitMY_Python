import reversion

from django.db import models
from ..company import Company
from benefit_plan import BenefitPlan

S = ["individual",
     "individual_plus_spouse",
     "individual_plus_family",
     "individual_plus_children",
     "individual_plus_one"]

TYPES = ([(item, item) for item in S])

@reversion.register
class CompanyBenefitPlanOption(models.Model):
    total_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=2)
    employee_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=10)
    benefit_option_type = models.TextField(choices=TYPES)

    company = models.ForeignKey(Company,
                                related_name="company_benefit",
                                blank=True,
                                null=True)
    benefit_plan = models.ForeignKey(BenefitPlan,
                                     related_name="company_benefit",
                                     blank=True,
                                     null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
