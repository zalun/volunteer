"""
person.models
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


class Profile(BaseModel):
    """Every person's profile
    """
    #:
    user = models.OneToOneField(User)
    #:
    phone = models.CharField(max_length=100, blank=True, default='')
    #:
    address = models.TextField(blank=True, default='')
    #:
    created_by = models.ForeignKey(User, related_name='people')
    #:
    created_at = models.DateTimeField(auto_now_add=True)
    #:
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    #:
    date_of_birth = models.DateField()

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
