from rest_framework import serializers

from .models import Drink


class DrinkSerializer(serializers.ModelSerializer):
    # ???
    # did it but don't know how it works
    creator = serializers.CharField(source='createdBy.username', read_only=True)
    class Meta:
        model = Drink
        fields = ['uuid', 'name', 'description', 'createdBy', 'is_publishable', 'creator']

        extra_kwargs = {'createdBy': {'write_only': True}}