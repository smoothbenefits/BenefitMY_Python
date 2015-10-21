import reversion

from django.db import models
from company_commuter_plan import CompanyCommuterPlan

from ..person import Person


@reversion.register
class PersonCompanyCommuterPlan(models.Model):

    company_commuter_plan = models.ForeignKey(
        CompanyCommuterPlan,
        related_name="person_company_commuter_plan")

    person = models.ForeignKey(
        Person,
        related_name="person_company_commuter_plan")

    monthly_amount_transit_pre_tax = models.DecimalField(max_digits=20, decimal_places=10)
    monthly_amount_transit_post_tax = models.DecimalField(max_digits=20, decimal_places=10)
    monthly_amount_parking_pre_tax = models.DecimalField(max_digits=20, decimal_places=10)
    monthly_amount_parking_post_tax = models.DecimalField(max_digits=20, decimal_places=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
