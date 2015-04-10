from django.db import models
from person import Person
from company import Company

import reversion

US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
    'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
    'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR',
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
    'WI', 'WY']

STATES_CHOICES = sorted([(item, item) for item in US_STATES])

@reversion.register
class Address(models.Model):
    address_type = models.CharField(max_length=255, null=True)
    street_1 = models.CharField(max_length=255)
    street_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(choices=STATES_CHOICES,
                             default='AL',
                             max_length=3)

    zipcode = models.CharField(max_length=10)
    person = models.ForeignKey(Person,
                               related_name='addresses',
                               blank=True,
                               null=True)
    company = models.ForeignKey(Company,
                                related_name='addresses',
                                blank=True,
                                null=True)
