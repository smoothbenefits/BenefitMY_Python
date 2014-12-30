from django.db import models
from company import Company
from benefit_type import BenefitType
from django.contrib.auth.models import User

class UserCompanyWaivedBenefit(models.Model):

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    benefit_type = models.ForeignKey(BenefitType)
