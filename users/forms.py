from django import forms


class ProfileAddressForm(forms.Form):
    fullname = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))
    address1 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }))
    address2 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }))
    pincode = forms.CharField(max_length=100, widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
        }))
    state = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }))
    country = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }))
    phonenumber = forms.CharField(max_length=100, widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
        }))


class verifyConnForm(forms.Form):
    pass
