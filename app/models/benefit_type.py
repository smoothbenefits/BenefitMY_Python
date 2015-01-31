from django.db import models

TYPES = (('Medical', 'Medical'),
         ('Dental', 'Dental'),
         ('Vision', 'Vision'),
         ('Life', 'Life'))


class BenefitType(models.Model):
    name = models.CharField(max_length=255, choices=TYPES)
