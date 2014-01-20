from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        date_joined = extra_fields.pop('date_joined', timezone.now())
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            date_joined=date_joined,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update({
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
        })
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True, max_length=511)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
