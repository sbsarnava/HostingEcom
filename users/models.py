from django.db import models
from django.contrib.auth.models import User
from shop.models import Order


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.IntegerField(null=True, blank=True, unique=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    panelAccountCreated = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username
