"""
base.forms
----------
"""
import logging

from django import forms
from django.contrib.auth.models import User

from base.models import MadeByModel

_log = logging.getLogger('volunteer.%s' % __name__)


class MadeByForm(forms.ModelForm):
    """Override created_by and modified_by fields with existing user,
    User() or None
    """

    class Meta:
        model = MadeByModel

    def clean_created_by(self):
        if self.instance and hasattr(self.instance, 'created_by'):
            return self.instance.created_by or User()
        return User()

    def clean_modified_by(self):
        if self.instance and hasattr(self.instance, 'created_by') and self.instance.created_by:
            return User()
        return None
