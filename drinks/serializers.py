from rest_framework import serializers

from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
    # describing the model
    class Meta:
        model = Drink
        fields = ['id', 'name', 'description']