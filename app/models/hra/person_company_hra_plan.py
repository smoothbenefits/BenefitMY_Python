import reversion

from django.db import models
from company_hra_plan import CompanyHraPlan

from app.custom_authentication import AuthUser
from ..person import Person

@reversion.register
class PersonCompanyHraPlan(models.Model):

    company_hra_plan = models.ForeignKey(
        CompanyHraPlan,
        related_name="person_company_hra_plan")

    person = models.ForeignKey(
        Person,
        related_name="person_company_hra_plan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
