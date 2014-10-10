from django.db import models
#from company_users import company_users


class User(models.Model):
    full_name = models.TextField()
    email = models.EmailField(max_length=255)
    encrypted_password = models.TextField()
    tz = models.TextField()
