"""
livery.forms
------------
"""
import logging

from base.forms import MadeByForm
from livery.models import Lending, Item

_log = logging.getLogger('volunteer.%s' % __name__)


class ItemForm(MadeByForm):

    class Meta:
        model = Item


class LendingForm(MadeByForm):

    class Meta:
        model = Lending
