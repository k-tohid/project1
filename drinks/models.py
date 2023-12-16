from django.db import models

from django.contrib.auth.models import User
from users.models import CustomUser


class Drink(models.Model):
    uuid = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.FloatField(blank=False)
    is_publishable = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
