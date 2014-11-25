from django.db import models


class BenefitPolicyKey(models.Model):
    name = models.CharField(max_length=255)

