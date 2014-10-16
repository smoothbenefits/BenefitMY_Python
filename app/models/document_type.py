from django.db import models


class DocumentType(models.Model):
    name = models.TextField()
