
from django.contrib.auth.models import User as AuthUser

import reversion

@reversion.register
class User(AuthUser):
    class Meta:
        proxy = True
