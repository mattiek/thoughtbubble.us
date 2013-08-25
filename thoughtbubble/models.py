from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )

class ThoughtbubbleUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    location=None,
                    password=None):
        if not username:
            msg = 'Users must have a username'
            raise ValueError(msg)

        user = self.model(
            username=username,
            email=ThoughtbubbleUserManager.normalize_email(email),
            location=location
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         username,
                         email,
                         password):
        user = self.create_user(username,
                                email,
                                password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ThoughtbubbleUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, default="", unique=True, db_index=True)
    email = models.CharField(max_length=254, default="", unique=True)
    location = models.CharField(max_length=50, default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = ThoughtbubbleUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return "{0} - {1}".format(self.email,
                                  self.username)

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.get_short_name()