from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/orders', profile_orders, name='profile-orders'),
    path('profile/products', profile_products, name='profile-products'),
    path('profile/invoices', invoicelist, name='profile-invoicelist'),
    path('profile/invoices/<str:oid>', GenerateInvoice.as_view(), name='profile-invoice'),
    path('profile/settings', profile_settings, name='profile-settings'),
    path('profile/changeAPIsettings', changeAPISettings, name='change-API')
]
