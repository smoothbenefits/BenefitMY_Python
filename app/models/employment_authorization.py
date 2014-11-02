from django.db import models
from signature import Signature

WORKER_TYPE = (("Citizen", "CItizen"),
               ("Noncitizen", "Noncitizen"),
               ("PResident", "PResideng"),
               ("Aaw", "Aaw"))


class EmploymentAuthorization(models.Model):
    worker_type = models.CharField(max_length=30,
                                   choices=WORKER_TYPE)
    expiration_date = models.DateField()
    uscis_number = models.CharField(max_length=255)
    i_94 = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    signature = models.ForeignKey(Signature,
                                  related_name="employment_authorization",
                                  null=True,
                                  blank=True)
