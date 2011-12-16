"""
base.models
-----------
"""
import logging

from django.db import models, IntegrityError
from django.contrib.auth.models import User

_log = logging.getLogger('volunteer.%s' % __name__)


class BaseModel(models.Model):
    """Force validation and privileges tests before save

    Call ``default_{field_name}`` methods which are setting the default value
    of the field when creating a new instance. `(Original Source)
    <https://github.com/seanmonstar/FlightDeck/blob/apps/base/models.py>`_

    :Authors:

       * Created by Sean McArthur for Mozilla Addons Builder,
       * Modified by Piotr Zalewa for jsFiddle
    """
    class Meta:
        #:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Implements ``creating`` attribute to ``_state`` object to provide
        more accurate information than original ``adding``.
        """
        super(BaseModel, self).__init__(*args, **kwargs)
        self.set_state()

    def set_state(self, force_insert=False):
        self._state.creating = False if self.pk and not force_insert else True

    def save(self, **kwargs):
        """Implements ``creating`` attribute to ``_state`` field to provide
        more accurate information than original ``adding``.

        If creating a new instance call all ``default_{field_name}`` methods
        (which are defined in a subclass) to set default values.

        Call all ``update_{field_name}`` methads (which are defined in
        subclass) to set update values for every save.

        Validate model for every save by calling ``full_clean`` and
        ``check_privileges`` methods.
        """
        self.set_state(force_insert=kwargs.get('force_insert', False))
        if self._state.creating:
            for attrName in dir(self):
                if attrName.find('default_') != 0:
                    continue
                attr = getattr(self, attrName)
                if callable(attr):
                    field = attrName[8:]
                    try:
                        orig = getattr(self, field)
                    except:
                        # this method is working for fields not exposed
                        # in class definition
                        orig = None
                    if orig is None or orig == '':
                        attr()

        for attrName in dir(self):
            if attrName.find('update_') != 0:
                continue
            attr = getattr(self, attrName)
            if callable(attr):
                attr()

        self.full_clean()
        self.check_privileges(**kwargs)
        return super(BaseModel, self).save(**kwargs)

    def check_privileges(self, **kwargs):
        """ A placeholder for a method which should be overriden to check for
        privileges
        """
        pass


class MadeByModel(BaseModel):
    """Provides ``created_at``, ``modified_at``, ``created_by`` and
    ``modified_by`` fields with integrity validation

    ``*_by`` fields ``related_name`` attribute is created from subclass's
    application name and its class name. In example
    :class:`~library.models.Framework` created by
    :class:`~django.contrib.auth.User` may be accessed via collection
    ``User.created_library_frameworks``. This technique is described in
    `Django Doc
    <http://docs.djangoproject.com/en/1.3/topics/db/models/#be-careful-with-related-name>`_
    """
    class Meta:
        #:
        abstract = True
    #: :class:`django.contrib.auth.models.User` object
    created_by = models.ForeignKey(User,
            related_name='created_%(app_label)s_%(class)ss', blank=True)
    #: :class:`django.contrib.auth.models.User` object (optional on create)
    modified_by = models.ForeignKey(User, null=True, blank=True,
            related_name='modified_%(app_label)s_%(class)ss')
    #:
    created_at = models.DateTimeField(auto_now_add=True)
    #:
    modified_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Checks if ``created_by`` or ``modified_by`` is *truthy*
        """
        error = True
        if self._state.creating and self.created_by:
            error = False
        if not self._state.creating and self.modified_by:
            error = False
        if error:
            msg = ("No author provided in %s (%s) (created_by: %s,"
                    " modified_by: %s)") % (self.__class__.__name__, self,
                            self.created_by, self.modified_by)
            _log.error(msg)
            raise IntegrityError(msg)
        return super(MadeByModel, self).clean()


class AssignedByModel(BaseModel):
    """Provides ``assigned_at``, ``assigned_by`` fields

    Inherit from this class to create fields which do need to record
    who has done the assignment.
    """
    class Meta:
        #:
        abstract = True
    #:
    assigned_at = models.DateTimeField(auto_now_add=True)
    #:
    assigned_by = models.ForeignKey(User, related_name='+')
