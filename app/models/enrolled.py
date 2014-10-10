from django.db import models


class Document(models.Model):
    user_company_benefit_plan_option_id = models.IntegerField()    
    person_id = models.IntegerField()    
