from rest_framework import serializers

from .models import Drink
from .helpers import create_uuid


class DrinkSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['uuid'] = create_uuid()
        validated_data['createdBy'] = self.context.get('user')
        return super().create(validated_data)
    creator = serializers.CharField(source='createdBy.username', read_only=True)
    class Meta:
        model = Drink
        fields = ['uuid', 'name', 'description', 'createdBy', 'is_publishable', 'creator']

        extra_kwargs = {'createdBy': {'write_only': True}, 'uuid': {'read_only': True}}