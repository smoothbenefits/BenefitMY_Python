import reversion

from django.db import models
from company import Company
from upload import Upload


@reversion.register
class Template(models.Model):
    company = models.ForeignKey(Company,
                                related_name="template")
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    upload = models.ForeignKey(Upload,
                               blank=True,
                               null=True,
                               related_name='template_uploads')
