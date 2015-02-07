from django.db import models
from company import Company
from life_insurance_plan import LifeInsurancePlan

S = ["individual",
     "individual_plus_spouse",
     "individual_plus_family",
     "individual_plus_children"]

TYPES = ([(item, item) for item in S])


class CompanyLifeInsurancePlan(models.Model):
    total_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=2)
    employee_cost_per_period = models.DecimalField(
        max_digits=20, decimal_places=2)
    benefit_option_type = models.TextField(choices=TYPES)
    company = models.ForeignKey(Company,
                                related_name="company_life_insurance",
                                blank=True,
                                null=True)
    life_insurance_plan = models.ForeignKey(LifeInsurancePlan,
                                            related_name="company_life_insurance",
                                            blank=True,
                                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
