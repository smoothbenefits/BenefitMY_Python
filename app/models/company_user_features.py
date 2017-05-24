from django.db import models
from company_user import CompanyUser
from sys_application_feature import SysApplicationFeature


class CompanyUserFeatures(models.Model):
    company_user = models.ForeignKey(CompanyUser)
    feature = models.ForeignKey(SysApplicationFeature)
    feature_status = models.BooleanField(default=True)
