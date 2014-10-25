from django.db import models
from user import User
from company import Company
from benefit_type import BenefitType


class UserCompanyWaivedBenefit(models.Model):

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    benefit_type = models.ForeignKey(BenefitType)
