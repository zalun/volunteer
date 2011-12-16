"""
person.forms
------------
"""
import logging

#from django.contrib import admin
from django import forms
from django.contrib.auth.forms import (UserChangeForm as _UserChangeForm,
                                        UserCreationForm)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from person.models import Profile

_log = logging.getLogger('volunteer.%s' % __name__)


class ProfileAdminForm(forms.ModelForm):

    fieldsets = [
            ('Profile settings', {
                'classes': ('collapse', ),
                'fields': ('phone', 'address', 'gender', 'date_of_birth')})]

    class Meta:
        model = Profile
        exclude = ('user', 'created_by')


class UserAddForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"),
            widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
            widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))
    fieldsets = [
            (None, {
                'fields': ['first_name', 'last_name']}),
            ('User settings', {
                'fields': ['username', 'password1', 'password2', 'email',
                    'is_staff', 'groups']})
            ]
    class Meta:
        model = User
        exclude = ('date_joined', 'last_login', 'password')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
                _("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                    _("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(_UserChangeForm):

    fieldsets = [
            (None, {
                'fields': ['first_name', 'last_name']}),
            ('User settings', {
                'classes': ('collapse',),
                'fields': ['username', 'email', 'password', 'groups',
                    'date_joined', 'is_staff', 'last_login']}),
            ]

    class Meta(_UserChangeForm.Meta):
        exclude = ('is_superuser', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['last_login'].widget.attrs['readonly'] = True
        self.fields['date_joined'].widget.attrs['readonly'] = True

    def clean_last_login(self):
        return self.instance.last_login

    def clean_date_joined(self):
        return self.instance.date_joined
