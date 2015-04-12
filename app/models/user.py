import reversion

from django.contrib.auth.models import User as AuthUser

@reversion.register
class User(AuthUser):
    class Meta:
        proxy = True
