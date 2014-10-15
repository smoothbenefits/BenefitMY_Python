from django.db import models


class Person(models.Model):
    obj_type = models.TextField(null=True)    
    person_type = models.CharField(max_length=30) 
    full_name = models.TextField(null=True)
    email = models.EmailField(max_length=255, null=True)
    relationship = models.CharField(max_length=30, null=True)
    ssn = models.TextField(null=True)
    birth_date = models.DateField(null=True)


