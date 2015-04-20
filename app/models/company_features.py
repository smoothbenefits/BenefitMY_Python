from django.db import models
from company import Company
from sys_application_feature import SysApplicationFeature


class CompanyFeatures(models.Model):
    company = models.ForeignKey(Company)
    company_feature = models.ForeignKey(SysApplicationFeature)
    feature_status = models.BooleanField(default=True)
