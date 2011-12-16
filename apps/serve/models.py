"""
serve.models
-------------
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from base.models import BaseModel

_log = logging.getLogger('volunteer.%s' % __name__)


GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'))


class Volunteer(BaseModel):
    """Profile for the volunteer
    """
    #:
    user = models.OneToOneField(User, related_name='volunteer')
    #:
    is_active = models.BooleanField(blank=True, default=True)
    #:
    description = models.TextField(blank=True, default='')
    #:
    created_by = models.ForeignKey(User, related_name='volunteers')
    #:
    created_at = models.DateTimeField(auto_now_add=True)
    #: comma separated list - will be changed to tags in the future
    skills = models.TextField(blank=True, default='',
            help_text='Comma separated list of skills')

    def __unicode__(self):
        return self.user


class Ward(BaseModel):
    """Profile for the ward
    """
    #:
    user = models.OneToOneField(User, related_name='ward')
    #:
    is_active = models.BooleanField(blank=True, default=True)
    #:
    description = models.TextField(blank=True, default='')
    #:
    created_by = models.ForeignKey(User, related_name='wards')
    #:
    created_at = models.DateTimeField(auto_now_add=True)
    #: comma separated list - will be changed to tags in the future
    needed_skills = models.TextField(blank=True, default='',
            help_text='Comma separated list of skills needed')
    #: comma separated list - will be changed to tags in the future
    issues = models.TextField(blank=True, default='',
            help_text='Comma separated list of issues (health, social, etc)')
