"""
livery.admin
------------
"""
import logging

from django.contrib import admin
#from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from livery.forms import LendingForm, ItemForm
from livery.models import ItemKind, Item, Lending

csrf_protect_m = method_decorator(csrf_protect)
_log = logging.getLogger('volunteer.%s' % __name__)


admin.site.register(ItemKind)

class LendingAdmin(admin.ModelAdmin):
    form = LendingForm
admin.site.register(Lending, LendingAdmin)

class LendingInline(admin.StackedInline):
    form = LendingForm
    model = Lending
    max_num = 1

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        return super(LendingInline, self).save_model(request, obj, form, change)

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    inlines = [LendingInline, ]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = None
        return super(ItemAdmin, self).save_model(request, obj, form, change)
admin.site.register(Item, ItemAdmin)
