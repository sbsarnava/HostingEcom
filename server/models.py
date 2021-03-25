from django.db import models
from django_cryptography.fields import encrypt


# Create your models here.
class ServerDetails(models.Model):
    adminUsername=encrypt(models.CharField(max_length=20, null=True))
    adminPassword = encrypt(models.CharField(max_length=20, null=True))
    server_url = models.URLField(null=True, unique=True)

    def __str__(self):
        return str(self.adminUsername)
