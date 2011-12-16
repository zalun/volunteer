"""
livery.admin
------------
"""
import logging

from django.contrib import admin

from base.forms import MadeByForm

_log = logging.getLogger('volunteer.%s' % __name__)

class MadeByAdmin(admin.ModelAdmin):
    form = MadeByForm

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = None
        return super(MadeByAdmin, self).save_model(request, obj, form, change)
