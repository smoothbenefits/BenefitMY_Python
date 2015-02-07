from django.db import models
from django.contrib.auth.models import User
from person import Person


class FSA(models.Model):
    amount_per_year = models.DecimalField(
        max_digits=8, decimal_places=2)

    user = models.ForeignKey(User,
                             related_name="fsa")
    person = models.ForeignKey(Person,
                               related_name="fsa")


    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
