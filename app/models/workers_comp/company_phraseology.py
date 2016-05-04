from django.db import models
from ..company import Company
from phraseology import Phraseology

class CompanyPhraseology(models.Model):
    company = models.ForeignKey(Company, related_name='company_company_phraseology')
    phraseology = models.ForeignKey(Phraseology, related_name='phraseology_company_phraseology')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
