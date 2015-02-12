from django.db import models
from django.contrib.auth.models import User
from person import Person


class FSA(models.Model):
    amount_per_year = models.DecimalField(
        max_digits=8, decimal_places=2)

    user = models.ForeignKey(User,
                             related_name="fsa")
    person = models.ForeignKey(Person,
                               unique=True,
                               related_name="fsa",
                               blank=True,
                               null=True)

    update_reason = models.CharField(max_length=1024, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
