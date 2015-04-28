import reversion

from django.db import models
from app.custom_authentication import AuthUser
from app.models.company import Company

upload_types = ["I9",
                "Deposit",
                "Manager",
                "MedicalBenefit",
                "DentalBenefit",
                "VisionBenefit"]

TYPES = ([(item, item) for item in upload_types])

@reversion.register
class Upload(models.Model):
    upload_type = models.TextField(choices=TYPES)
    user = models.ForeignKey(AuthUser, related_name="user_upload")
    company = models.ForeignKey(Company, related_name="company_upload")
    S3 = models.CharField(max_length=2048)    # S3 link
    file_name = models.CharField(max_length=2048, blank=True, null=True)
    file_type = models.CharField(max_length=128, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
