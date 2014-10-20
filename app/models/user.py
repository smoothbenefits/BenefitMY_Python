from django.contrib.auth.models import User as AuthUser


class User(AuthUser):
    class Meta:
        proxy = True
