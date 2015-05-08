import reversion

from django.db import models
from ..person import Person
from company_supplemental_life_insurance_plan import CompanySupplementalLifeInsurancePlan

@reversion.register
class PersonCompanySupplementalLifeInsurancePlan(models.Model):

    company_supplemental_life_insurance_plan = models.ForeignKey(CompanySupplementalLifeInsurancePlan,
                                                                 related_name="person_company_supplemental_life_insurance_plan")

    person = models.ForeignKey(Person,
                               related_name="person_company_supplemental_life_insurance_plan")

    self_elected_amount = models.DecimalField(max_digits=10, 
                                              decimal_places=2,
                                              blank=True,
                                              null=True)

    spouse_elected_amount = models.DecimalField(max_digits=10, 
                                                decimal_places=2,
                                                blank=True,
                                                null=True)

    child_elected_amount = models.DecimalField(max_digits=10, 
                                               decimal_places=2,
                                               blank=True,
                                               null=True)

    self_premium_per_month = models.DecimalField(max_digits=10, 
                                                 decimal_places=2, 
                                                 blank=True,
                                                 null=True,
                                                 verbose_name="calculated premium for self")

    spouse_premium_per_month = models.DecimalField(max_digits=10, 
                                                   decimal_places=2, 
                                                   blank=True,
                                                   null=True,
                                                   verbose_name="calculated premium for spouse")

    child_premium_per_month = models.DecimalField(max_digits=10, 
                                                  decimal_places=2, 
                                                  blank=True,
                                                  null=True,
                                                  verbose_name="calculated premium for child")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
