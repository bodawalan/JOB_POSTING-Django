from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager

# Create your models here.
class JobPosting(models.Model):
    title=models.CharField(max_length=100)
    number_of_position=models.IntegerField()
    level=models.CharField(max_length=100,choices=(('S', 'SeniorLevel'),
                                    ('M', 'MidLevel'),
                                    ('J', 'JuniorLevel')))

    posting_date=models.DateField()
    desciption=models.TextField(max_length=2000)


class Filter(models.Model):

    level=models.ManyToManyField(JobPosting)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    name = models.CharField(_('last name'), max_length=30, blank=True)
    is_organization = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
