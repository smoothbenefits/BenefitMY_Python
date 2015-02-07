from django.db import models
from user_company_life_insurance_plan import UserCompanyLifeInsurancePlan
from person import Person


class LifeInsuranceEnrolled(models.Model):
    user_company_life_insurance_plan = models.ForeignKey(
        UserCompanyLifeInsurancePlan,
        related_name="life_insurance_enrolleds")
    person = models.ForeignKey(Person,
                               related_name="life_insurance_enrolleds")
    insurance_amount = models.DecimalField(
        max_digits=20, decimal_places=2)
