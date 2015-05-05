import reversion

from django.db import models
from signature import Signature
from app.custom_authentication import AuthUser

WORKER_TYPE = (("Citizen", "Citizen"),
               ("Noncitizen", "Noncitizen"),
               ("PResident", "PResident"),
               ("Aaw", "Aaw"))

@reversion.register
class EmploymentAuthorization(models.Model):
    worker_type = models.CharField(max_length=30,
                                   choices=WORKER_TYPE)
    expiration_date = models.DateField(blank=True, null=True)
    uscis_number = models.CharField(max_length=255, blank=True, null=True)
    i_94 = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    signature = models.ForeignKey(Signature,
                                  related_name="employment_authorization",
                                  null=True,
                                  blank=True)

    user = models.ForeignKey(AuthUser,
                             related_name="employment_authorization")
