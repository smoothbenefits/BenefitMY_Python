from django.db import models


class CompanyUser(models.Model):
    user_id = models.IntegerField()
    company_id = models.IntegerField()
    company_user_type = models.TextField()
