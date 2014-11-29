from django.db import models


class BenefitPolicyType(models.Model):
    name = models.CharField(max_length=255)

