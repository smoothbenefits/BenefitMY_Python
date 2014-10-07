from django.db import models

US_STATES =[
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
        'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
        'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
        'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR',
        'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
        'WI', 'WY']

STATES_CHOICES = sorted([(item, item) for item in US_STATES])


class Address(models.Model):
    street_1 = models.TextField()
    street_2 = models.TextField(blank=True)
    city = models.TextField()
    state = models.CharField(choices=STATES_CHOICES,
                             default='AL',
                             max_length=3)

    zipcode = models.TextField()

    class Meta:
        app_label = 'app'
