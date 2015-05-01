import reversion

from django.db import models
from app.custom_authentication import AuthUser

@reversion.register
class FsaPlan(models.Model):

    broker_user = models.ForeignKey(AuthUser,
                                    related_name="fsa_plan")
    name = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
