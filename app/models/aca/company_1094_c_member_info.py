import reversion
from django.db import models
from app.models.company import Company

ELIGIBILITY_CERTIFICATIONS = ['Qualifying Offer Method',
                              'Qualifying Offer Method Transition Relief',
                              'Section 4980H Transition Relief',
                              '98 Percent Offer Method']

CERTIFICATION_CHOICES = ([(item, item) for item in ELIGIBILITY_CERTIFICATIONS])

@reversion.register
class Company1094CMemberInfo(models.Model):
    company = models.ForeignKey(Company, related_name="company_1094C")
    number_of_1095c = models.PositiveIntegerField(default=0)
    authoritative_transmittal = models.BooleanField(default=False)
    member_of_aggregated_group = models.BooleanField(default=False)
    certifications_of_eligibility = models.CharField(choices=CERTIFICATION_CHOICES,
                                                     default='Qualifying Offer Method',
                                                     max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
