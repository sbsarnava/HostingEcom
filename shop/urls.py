from django.urls import path
from .views import *

app_name = 'shop'
urlpatterns = [
    path('', index, name='index'),
    path('store/', store, name='store'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout, name='checkout'),
    path('cart/', cart, name='cart'),
    path('cashpayment/', cash_payment, name='cash-payment'),
    path('razorpayment/', razorpay_payment, name='razor-payment'),
    path('getAddress/', getAddress, name='get-address')
]
