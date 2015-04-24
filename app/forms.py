from django import forms
from app.custom_authentication import AuthUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ('email', 'password')
