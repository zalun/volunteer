"""
office.models
-------------
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from base.models import BaseModel

from serve.models import Volunteer

_log = logging.getLogger('volunteer.%s' % __name__)


class Opinion(BaseModel):
    """A single opinion about a Volunteer
    """
    #:
    manager = models.ForeignKey(User, related_name='opinons about others')
    #:
    volunteer = models.ForeignKey(Volunteer, related_name='opinions')
    #:
    content = models.TextField()
    #:
    rating = models.IntegerField(blank=True, null=True,
            help_text=_('0 - very bad, 9 - super fantastic'))


