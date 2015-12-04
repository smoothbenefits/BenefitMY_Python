from django.db import models
from company_group import CompanyGroup
from app.custom_authentication import AuthUser

class CompanyGroupMember(models.Model):
    company_group = models.ForeignKey(CompanyGroup, on_delete=models.CASCADE, related_name="company_group_members")
    user = models.ForeignKey(AuthUser, related_name="company_group_user")
    created = models.DateTimeField(auto_now_add=True, null=True)
