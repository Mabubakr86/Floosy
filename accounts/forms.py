from django import forms
from .models import Account
from django_countries.fields import CountryField


class AccountForm(forms.ModelForm):
    country = CountryField().formfield()

    class Meta:
        model = Account
        exclude = ['user']
