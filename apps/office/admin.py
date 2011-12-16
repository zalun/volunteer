"""
office.admin
------------
"""
import logging

from django.contrib import admin

from office.models import Opinion

_log = logging.getLogger('volunteer.%s' % __name__)


admin.site.register(Opinion)
