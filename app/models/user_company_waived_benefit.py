from django.db import models
from app.model.user import User
from app.model.company import Company
from app.model.benefit_type import BenefitType


class UserCompanyWaivedBenefit(models.Model):

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    benefit_type = models.ForeignKey(BenefitType)
