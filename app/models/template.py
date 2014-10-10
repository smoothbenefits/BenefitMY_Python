from django.db import models


class Template(models.Model):
    company_id = models.IntegerField()
    document_type_id = models.IntegerField()
    name = models.TextField()
    content = models.TextField()
