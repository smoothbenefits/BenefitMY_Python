from django.db import models


class Document(models.Model):
    company_id = models.IntegerField()    
    user_id = models.IntegerField()    
    template_id = models.IntegerField()    
    document_type_id = models.IntegerField()    
    name = models.TextField()    
    content = models.TextField()  
    edited = models.BooleanField(default=False)  
