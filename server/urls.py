from django.urls import path
from .views import *
app_name = 'server'
urlpatterns = [
    path('', server_index)
]