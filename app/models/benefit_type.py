from django.db import models

TYPES = (('Medical', 'Medical'),
         ('Dental', 'Dental'),
         ('Vision', 'Vision'))


class BenefitType(models.Model):
    name = models.TextField(choices=TYPES)
    display_priority = models.IntegerField()
