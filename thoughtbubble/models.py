from django.conf import settings
from django.db import models
from thoughtbubble.utils import path_and_rename
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )
from avatar.models import Avatar
from geo.organization.models import Organization
import itertools


class ThoughtbubbleUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None):
        if not username:
            msg = 'Users must have a username'
            raise ValueError(msg)

        user = self.model(
            username=username.lower(),
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


    def is_curator(self, org):
        d = None
        s = False
        if self.is_superuser:
            s = True
        else:
            list_of_curators = list(self.organizationcurator_set.all())
            d = []
            for i in list_of_curators:
                for r in i.organization_curator.all():
                    if r.pk == org.pk:
                        return True

                    # x = [i.organization_curator.all() for i in list_of_curators]
                    #
                    # # unravelling from a list
                    # d = itertools.chain(*x)
                    #
                    # if not len(d):
                    #     d = None

        return s

    def get_curated_orgs(self):
        d = None
        if self.is_superuser:
            d = Organization.objects.all()
        else:
            list_of_curators = list(self.organizationcurator_set.all())
            d = []
            for i in list_of_curators:
                for r in i.organization_curator.all():
                    d.append(r)

            # x = [i.organization_curator.all() for i in list_of_curators]
            #
            # # unravelling from a list
            # d = itertools.chain(*x)
            #
            # if not len(d):
            #     d = None

        return d


    def __unicode__(self):
        return self.get_short_name()



from geo.places.models import Region

class ThoughtbubbleUserProfile(models.Model):
    user = models.OneToOneField(ThoughtbubbleUser)
    first_name = models.CharField(max_length=50, default="", null=True, blank=True)
    last_name = models.CharField(max_length=50, default="", null=True, blank=True)
    location = models.CharField(max_length=50, default="", null=True, blank=True)
    profile_picture = models.ImageField(upload_to=path_and_rename('profiles', 'profile_picture'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    region = models.ForeignKey(Region, null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % (self.user.username,)



