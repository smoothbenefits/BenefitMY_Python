from django.db import models
from company import Company
from benefit_plan import BenefitPlan

S = ["individual",
     "individual_plus_spouse",
     "individual_plus_family",
     "individual_plus_children"]

TYPES = ([(item, item) for item in S])


class CompanyBenefitPlanOption(models.Model):
    total_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=2)
    employee_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=2)
    benefit_option_type = models.TextField(choices=TYPES)

    company = models.ForeignKey(Company,
                                related_name="company_benefit",
                                blank=True,
                                null=True)
    benefit_plan = models.ForeignKey(BenefitPlan,
                                     related_name="company_benefit",
                                     blank=True,
                                     null=True)
    pcp_link = models.CharField(max_length=1024,
                                blank=True,
                                null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
