from email.policy import default

from django import forms
from .models import BillingAddress, Country


class BillingForm(forms.Form):
    firstname = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }
    ))
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }
    ))
    phonenumber = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'email',
            'onchange': 'edited()'
        }
    ))
    address1 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }
    ))
    address2 = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }))

    city = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }))

    state = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }
    ))

    pincode = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onchange': 'edited()'
        }))
    # same_as_shipping = forms.BooleanField(widget=forms.CheckboxInput(
    #     attrs={
    #         'class': 'custom-control-input',
    #         'type': 'checkbox'
    #     }
    # ), initial=False)
    saveAddress = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class': 'custom-control-input',
            'type': 'checkbox'
        }
    ), initial=False)

    country = forms.ChoiceField(choices=[('', '')],
                                widget=forms.Select(attrs={
                                    'class': 'custom-select d-block w-100',
                                    'onchange': 'edited()'
                                }))

    payment = forms.CharField(widget=forms.RadioSelect(attrs={'class': 'custom-input'}, choices=[
        ('cash', 'Cash on Delivery'),
        ('razorpay', 'Card/Net Banking/UPI')]),
                              max_length=100)

    def __init__(self, *args, **kwargs):
        super(BillingForm, self).__init__(*args, **kwargs)
        self.fields['saveAddress'].required = False
        self.fields['email'].required = False
        self.fields['address2'].required = False
        self.fields['country'].choices = [(item, item) for item in Country.objects.all()]
