from django.db import models
from company import Company
from company_feature_list import CompanyFeatureList


class CompanyFeatures(models.Model):
    company = models.ForeignKey(Company)
    company_feature = models.ForeignKey(CompanyFeatureList)
    feature_status = models.BooleanField(default=True)
