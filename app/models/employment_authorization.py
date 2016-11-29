import reversion

from django.db import models
from signature import Signature
from app.custom_authentication import AuthUser

WORKER_TYPE_CITIZEN = "Citizen"
WORKER_TYPE_NONCITIZEN = "Noncitizen"
WORKER_TYPE_PERM_RESIDENT = "PResident"
WORKER_TYPE_AAW = "Aaw"

WORKER_TYPE = ((WORKER_TYPE_CITIZEN, WORKER_TYPE_CITIZEN),
               (WORKER_TYPE_NONCITIZEN, WORKER_TYPE_NONCITIZEN),
               (WORKER_TYPE_PERM_RESIDENT, WORKER_TYPE_PERM_RESIDENT),
               (WORKER_TYPE_AAW, WORKER_TYPE_AAW))

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
