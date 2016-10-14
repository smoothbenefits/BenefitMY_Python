import reversion

from django.db import models
from company import Company
from app.custom_authentication import AuthUser
from encrypted_fields import EncryptedTextField

GENDER_TYPES = ([(item, item) for item in ['F', 'M']])
SELF = 'self'
DEPENDENT = 'dependent'
SPOUSE = 'spouse'
CHILD = 'child'
LIFE_PARTNER = 'life partner'
EX_SPOUSE = 'ex-spouse'
DISABLED_DEPENDENT = 'disabled dependent'
STEP_CHILD = 'stepchild'
RELATIONSHIPS = ((SELF, 'self'),
                 (DEPENDENT, 'dependent'),
                 (SPOUSE, 'spouse'),
                 (CHILD, 'child'),
                 (LIFE_PARTNER, 'life partner'),
                 (EX_SPOUSE, 'ex-spouse'),
                 (DISABLED_DEPENDENT, 'disabled dependent'),
                 (STEP_CHILD, 'stepchild'))

@reversion.register
class Person(models.Model):
    person_type = models.CharField(max_length=30, db_index=True)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    relationship = models.CharField(max_length=30, choices=RELATIONSHIPS, default=DEPENDENT, db_index=True)
    ssn = EncryptedTextField(null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    reason_for_change = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=2,
                              choices=GENDER_TYPES,
                              null=True,
                              blank=True)

    user = models.ForeignKey(AuthUser,
                             related_name="family",
                             null=True,
                             blank=True)
    company = models.ForeignKey(Company,
                                related_name="contacts",
                                null=True,
                                blank=True)
