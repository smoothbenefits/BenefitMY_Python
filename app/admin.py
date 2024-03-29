from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from app.custom_authentication import AuthUser
from app.models import (
    Company,
    CompanyUser,
    Person,
    SysPeriodDefinition,
    SysApplicationFeature,
    CompanyFeatures,
    CompanyUserFeatures,
    IntegrationProvider,
    CompanyIntegrationProvider
)
from app.models.system.email_block_list import EmailBlockList
from app.models.system.system_setting import SystemSetting
from app.models.integration.company_user_integration_provider import CompanyUserIntegrationProvider

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("You can change user's password using <a href=\"password/\">this form</a>."))

    class Meta:
        model = AuthUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AuthUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'is_superuser')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','pay_period_definition')
    fields = ['name', 'pay_period_definition']

class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'company_user_type', 'new_employee')
    fields = ['user', 'company', 'company_user_type', 'new_employee']

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'company')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'relationship')}),
        ('User Relation', {'fields': ('user',)}),
        ('Company Relation', {'fields': ('company',)}),
    )

class CompanyFeatureAdmin(admin.ModelAdmin):
    list_display = ('company', 'company_feature', 'feature_status')
    fields = ['company', 'company_feature', 'feature_status']

class CompanyUserFeatureAdmin(admin.ModelAdmin):
    list_display=('company_user','feature', 'feature_status')
    fields=['company_user', 'feature', 'feature_status']

class SysPeriodDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'month_factor')
    fields = ['name', 'month_factor']

class SysApplicationFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature',)
    fields = ['feature']

class EmailBlockListAdmin(admin.ModelAdmin):
    list_display=('email_block_feature', 'user')
    fields=['email_block_feature', 'user']

class SystemSettingAdmin(admin.ModelAdmin):
    list_display=('name', 'value')
    fields=['name', 'value']

class IntegrationProviderAdmin(admin.ModelAdmin):
    list_display=('name', 'service_type')
    fields=['name', 'service_type']

class CompanyIntegrationProviderAdmin(admin.ModelAdmin):
    list_display=('company', 'integration_provider', 'company_external_id', 'employee_external_id_seed')
    fields=['company', 'integration_provider', 'company_external_id', 'employee_external_id_seed']

class CompanyUserIntegrationProviderAdmin(admin.ModelAdmin):
    list_display=('company_user', 'integration_provider', 'company_user_external_id')
    fields=['company_user', 'integration_provider', 'company_user_external_id']

# Now register the new UserAdmin...
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(CompanyFeatures, CompanyFeatureAdmin)
admin.site.register(CompanyUserFeatures, CompanyUserFeatureAdmin)
admin.site.register(SysPeriodDefinition, SysPeriodDefinitionAdmin)
admin.site.register(SysApplicationFeature, SysApplicationFeatureAdmin)
admin.site.register(EmailBlockList, EmailBlockListAdmin)
admin.site.register(SystemSetting, SystemSettingAdmin)
admin.site.register(IntegrationProvider, IntegrationProviderAdmin)
admin.site.register(CompanyIntegrationProvider, CompanyIntegrationProviderAdmin)
admin.site.register(CompanyUserIntegrationProvider, CompanyUserIntegrationProviderAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
