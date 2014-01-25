from django.conf import settings
from django.db import models
from thoughtbubble.utils import path_and_rename
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )
from avatar.models import Avatar


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
        return self.thoughtbubbleuserprofile

    def get_profile_picture(self):
        avatar = Avatar.objects.get(user=self,primary=True)
        if avatar and avatar.avatar:
            return avatar.avatar.url
        return ""


    def get_social_account(self, provider):
        try:
            return self.socialaccount_set.get(provider=provider)
        except:
            return None

    def get_twitter_account(self):
        return self.get_social_account('twitter')

    def get_facebook_account(self):
        return self.get_social_account('facebook')

    def get_linkedin_account(self):
        return self.get_social_account('linkedin')


    def __unicode__(self):
        return self.get_short_name()


class ThoughtbubbleUserProfile(models.Model):
    user = models.OneToOneField(ThoughtbubbleUser)
    first_name = models.CharField(max_length=50, default="", null=True, blank=True)
    last_name = models.CharField(max_length=50, default="", null=True, blank=True)
    location = models.CharField(max_length=50, default="", null=True, blank=True)
    profile_picture = models.ImageField(upload_to=path_and_rename('profiles', 'profile_picture'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s's profile" % (self.user.username,)



