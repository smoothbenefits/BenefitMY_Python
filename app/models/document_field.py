from django.db import models


class DocumentField(models.Model):
    document_id = models.IntegerField()    
    name = models.TextField()    
    value = models.TextField()  
  
