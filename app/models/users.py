from django.db import models
from company_users import company_users


class Users(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
        
