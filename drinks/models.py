from django.db import models

from django.contrib.auth.models import User

class Drink(models.Model):
    uuid = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    is_publishable = models.BooleanField(default=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
