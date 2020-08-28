from django.contrib import admin
from .models import *


admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(PromoCode)
admin.site.register(BillingAddress)
admin.site.register(Country)
admin.site.register(ShippingAddress)
