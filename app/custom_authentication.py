from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class AuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
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
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def user_exists(self, email):
        return AuthUser.objects.filter(email=email).exists()

    def get_user(self, email):
        return AuthUser.objects.get(email=email)


class AuthUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        db_index=True,
        unique=True,
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
