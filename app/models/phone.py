from django.db import models


class Phone(models.Model):
    phone_type = models.TextField()
    number = models.TextField()

    class Meta:
        app_label = 'app'
