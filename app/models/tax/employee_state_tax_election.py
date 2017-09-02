import reversion

from django.db import models
from app.custom_authentication import AuthUser
from ..address import STATES_CHOICES


@reversion.register
class EmployeeStateTaxElection(models.Model):
    user = models.ForeignKey(AuthUser,
                             related_name="user_state_tax_elections")
    state = models.CharField(choices=STATES_CHOICES,
                             default='MA',
                             max_length=3)

    # This is to hold JSON representation of tax witholding data
    # Our current version of Django does not support Postgres JSONB
    # fields, so we are forced to just use text field. 
    # This should be ok for the purpose, as we do not expect queryability 
    # against the field values. 
    data = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = (('user', 'state'),)
