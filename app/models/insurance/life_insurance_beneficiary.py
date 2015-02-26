from django.db import models
from user_company_life_insurance_plan import UserCompanyLifeInsurancePlan
from ..person import Person

class LifeInsuranceBeneficiary(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    user_life_insurance_plan = models.ForeignKey(UserCompanyLifeInsurancePlan,
                                    related_name='life_insurance_beneficiary',
                                    blank=True,
                                    null=True)
    percentage = models.DecimalField(max_digits=5,
                                    decimal_places=2,
                                    null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
