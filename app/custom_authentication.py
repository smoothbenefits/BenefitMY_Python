from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class AuthUserManager(BaseUserManager):

    ''' Override this method from the BaseUserManager to
        overcome the default implementation that assumes
        case-sensitivity on username/email lookup.

        Django refuses to fix this due to backward compatibility concerns.
        Though as of Django 1.5, with the support of iexact derivative, the
        below workaround became possible

        See more details:
          * http://stackoverflow.com/questions/13190758/django-case-insensitive-matching-of-username-from-auth-user
          * https://code.djangoproject.com/ticket/2273#comment:12
          * https://djangosnippets.org/snippets/1368/
    '''
    # def get_by_natural_key(self, email):
    #     return self.get(email__iexact=email)

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email)
        )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def user_exists(self, email):
        return AuthUser.objects.filter(email=email).exists()

    def get_user(self, email):
        try:
            return AuthUser.objects.get(email=email)
        except AuthUser.DoesNotExist:
            return None


class AuthUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        db_index=True,
        unique=True,
        validators=[EmailValidator],
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # First and last name should only be used in registration email
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_active

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app?"
        return self.is_active

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
