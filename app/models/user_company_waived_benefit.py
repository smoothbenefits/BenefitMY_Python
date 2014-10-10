from django.db import models


class UserCompanyWaivedBenefit(models.Model):

    user_id = models.IntegerField()
    company_id = models.IntegerField()
    benefit_type_id = models.IntegerField()
