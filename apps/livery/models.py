"""
livery.models
-------------
"""
import datetime
import logging

#from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from base.models import BaseModel, MadeByModel

_log = logging.getLogger('volunteer.%s' % __name__)

class ItemKind(BaseModel):
    #:
    name = models.CharField(_('Name'), max_length=255,
            help_text=_('In example "wheelchair"'))

class Item(MadeByModel):
    #:
    kind = models.ForeignKey(ItemKind)
    #:
    ind = models.CharField(_('Index'), max_length=10)
    #:
    characteristic = models.CharField(_('Characteristics'), max_length=255,
            blank=True, null=True, help_text='Color, producer, etc.')
    #:
    description = models.TextField(_('Description'), max_length=255,
            blank=True, null=True)
    #:
    state = models.CharField(_('State'), max_length=255,
            help_text=_('In example "Good", "With scratches"'))
    #:
    is_available = models.BooleanField(_('Is it available?'), blank=True,
            default=True)

    def __unicode__(self):
        return "[%s] %s - %s/%s" % (self.ind, self.kind.name, self.created_by, self.modified_by)


class Lending(MadeByModel):
    """Record who and why borrowed the :class:`Item`
    """
    #:
    item = models.ForeignKey(Item)
    #: ID number or anything which is a proof of identity
    identity = models.CharField(_('ID'), max_length=255,
            help_text=_("Proof of identity"))
    #:
    purpose = models.CharField(_('Purpose'), max_length=255, blank=True,
            null=True)
    #:
    state = models.CharField(_('State'), max_length=100,
            help_text=_('In example "Good", "With scratches"'))
    #:
    lending_date = models.DateField(_('Lent'), default=datetime.date.today,
            help_text=_('Actual day when the item was lent'))
    #:
    is_returned = models.BooleanField(_('Is item returned?'), blank=True,
            default=False)
    #:
    return_date = models.DateField(_('Date of returning the item'), blank=True,
            null=True)
