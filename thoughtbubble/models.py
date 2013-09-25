from django.conf import settings
from django.db import models
from thoughtbubble.utils import path_and_rename
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )
from neighborhood.models import Neighborhood


class ThoughtbubbleUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None):
        if not username:
            msg = 'Users must have a username'
            raise ValueError(msg)

        user = self.model(
            username=username,
            email=ThoughtbubbleUserManager.normalize_email(email)
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

    def get_profile(self):
        return self.thoughtbubbleuserprofile_set.all()[0]

    def get_profile_picture(self):
        pic = self.get_profile().profile_picture
        if pic:
            return pic.url
        return None

    def __unicode__(self):
        return self.get_short_name()


class ThoughtbubbleUserProfile(models.Model):
    user = models.ForeignKey(ThoughtbubbleUser)
    first_name = models.CharField(max_length=50, default="", null=True, blank=True)
    last_name = models.CharField(max_length=50, default="", null=True, blank=True)
    location = models.CharField(max_length=50, default="", null=True, blank=True)
    profile_picture = models.ImageField(upload_to=path_and_rename('profiles', 'profile_picture'), null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % (self.user.username,)


