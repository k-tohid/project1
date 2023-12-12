from rest_framework import serializers

from .models import Drink
from .helpers import create_uuid


class DrinkSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='createdBy.username', read_only=True)

    class Meta:
        model = Drink
        fields = ['uuid', 'name', 'description', 'price', 'is_publishable', 'creator']
        read_only_fields = ['uuid', 'creator']

    def create(self, validated_data):
        validated_data['uuid'] = create_uuid()
        validated_data['createdBy'] = self.context.get('user')
        return super().create(validated_data)

    def to_representation(self, instance):
        """Warns about alcoholic drinks"""
        drink = super().to_representation(instance)
        if drink['name'].startswith('Al.'):
            drink['name'] = drink['name'].replace('Al.', 'Not for pregnant people,')
        return drink
