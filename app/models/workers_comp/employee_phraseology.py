from django.db import models
from ..person import Person
from phraseology import Phraseology

class EmployeePhraseology(models.Model):
    employee_person = models.ForeignKey(Person, related_name='employee_employee_phraseology')
    phraseology = models.ForeignKey(Phraseology, related_name='phraseology_employee_phraseology')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
