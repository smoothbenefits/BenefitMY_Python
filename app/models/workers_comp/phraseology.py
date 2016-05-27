from django.db import models

class Phraseology(models.Model):
    phraseology = models.CharField(max_length=2048)
    ma_code = models.CharField(max_length=4, null=True, blank=True)
