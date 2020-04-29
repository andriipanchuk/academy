from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class UpdateInfo(forms.Form):
    first_name = forms.CharField(min_length=2, max_length=30)
    last_name = forms.CharField(min_length=2, max_length=30)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(UpdateInfo, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        if not first_name or not last_name or not email:
            raise forms.ValidationError('Please enter required information')
