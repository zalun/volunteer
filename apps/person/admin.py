"""
person.admin
------------
"""
import logging

from django.contrib import admin
from django.contrib.admin import helpers # widgets,
from django.contrib.admin.util import unquote
from django.core.exceptions import PermissionDenied #, ValidationError
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.html import escape #, escapejs
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from person.forms import ProfileAdminForm, UserChangeForm, UserAddForm
from person.models import Profile

csrf_protect_m = method_decorator(csrf_protect)
_log = logging.getLogger('volunteer.%s' % __name__)


class ProfileAdmin(admin.ModelAdmin):

    form = ProfileAdminForm
    change_user_form = UserChangeForm
    add_user_form = UserAddForm

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        if request.method == 'POST':
            form = self.form(request.POST, request.FILES, prefix='profile')
            user_form = self.add_user_form(request.POST, prefix='user')

            if form.is_valid() and user_form.is_valid():
                new_user = user_form.save()
                new_profile = form.save(commit=False)
                new_profile.user = new_user
                new_profile.created_by = request.user
                new_profile.save()
                return self.response_add(request, new_profile)
        else:
            user_form = self.add_user_form(prefix='user')
            form = self.form(prefix='profile')

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        userAdminForm = helpers.AdminForm(user_form,
                user_form.fieldsets,
                {}, None, model_admin=self)

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'useradminform': userAdminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'errors': helpers.AdminErrorList(form, {}),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)


    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        """Modified :meth:`django.contrib.admin.options.ModelAdmin.change_view`
        """
        # here saving the User object
        model = self.model
        opts = model._meta

        profile = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, profile):
            raise PermissionDenied

        if profile is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url='../add/')

        if request.method == 'POST':
            user_form = self.change_user_form(request.POST, prefix='user', instance=profile.user)
            profile_form = self.form(request.POST,
                    request.FILES, prefix='profile', instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                new_user = user_form.save()
                profile_form.cleaned_data['user'] = new_user
                new_profile = profile_form.save()
                # save the messages
                return self.response_change(request, new_profile)
            else:
                _log.warning('Wrong input data')
                _log.warning(user_form.errors)
                new_user = profile.user
                new_profile = profile
        else:
            user_form = self.change_user_form(instance=profile.user, prefix='user')
            profile_form = self.form(instance=profile, prefix='profile')

        adminForm = helpers.AdminForm(profile_form, self.get_fieldsets(request, profile),
            self.prepopulated_fields, self.get_readonly_fields(request, profile),
            model_admin=self)
        media = self.media + adminForm.media

        userAdminForm = helpers.AdminForm(user_form,
                user_form.fieldsets,
                {}, None, model_admin=self)

        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': profile,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'errors': helpers.AdminErrorList(profile_form, {}),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
            'useradminform': userAdminForm
        }

        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=profile)

admin.site.register(Profile, ProfileAdmin)

