from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_default_group(self):
        return Group.objects.get(pk=1)


class Account(models.Model):
    user = models.OneToOneField(User, null=False)
    group = models.ForeignKey(Group, null=True, default=Group.get_default_group)
    is_group_admin = models.BooleanField(default=False, null=None)

    def __unicode__(self):
        return self.user.username


