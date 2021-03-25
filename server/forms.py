from django import forms
from django.db.models import fields
from .models import ServerDetails


class ServerDetailsForm(forms.ModelForm):
    class Meta:
        model = ServerDetails
        fields = ['server_url']

