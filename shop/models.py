from audioop import max
from datetime import datetime
from django.db import models
from django.contrib.sessions.models import Session
from django.conf import settings
from users.utils import randomNumber

ORDER_STATUS = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('completed', 'Completed'),
)


class Item(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    price = models.IntegerField()
    package_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            super(OrderItem, self).delete(*args, **kwargs)
        else:
            super(OrderItem, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.id} of {self.user}"


# Not Working now
class PromoCode(models.Model):
    promo = models.CharField(unique=True, max_length=100)
    startDate = models.DateTimeField(null=True, blank=True)
    stopDate = models.DateTimeField(null=True, blank=True)
    discount = models.FloatField()
    isPercentage = models.BooleanField(default=False)


class Country(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address1 = models.CharField(max_length=1000)
    address2 = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    saveAddress = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    orderId = models.CharField(max_length=10, default=randomNumber(), unique=True)
    cartItems = models.OneToOneField(Cart, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.now)
    placed_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    billingAddress = models.ForeignKey(BillingAddress, null=True, on_delete=models.SET_NULL)
    status = models.CharField(choices=ORDER_STATUS, default='processing', max_length=11)

    def __str__(self):
        return f"{self.user} - {self.placed_date}"
