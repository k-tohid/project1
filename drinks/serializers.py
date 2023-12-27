from rest_framework import serializers

from .models import Drink, DrinkImage
from .helpers import create_uuid


class DrinkImageSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=False),
                                            write_only=True, required=False)
    class Meta:
        model = DrinkImage
        fields = ['image', 'uploaded_images']

    def create(self, validated_data):
        drink = self.context['drink']
        images = validated_data['uploaded_images']

        for image in images:
            DrinkImage.objects.create(drink=drink, image=image)

        return 1


class DrinkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    creator = serializers.CharField(source='created_by.username', read_only=True)

    images = DrinkImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=False),
                                            write_only=True, required=False)

    class Meta:
        model = Drink
        fields = ['uuid', 'name', 'description', 'price', 'is_publishable', 'creator', 'created_on', "images",
                  "uploaded_images"]
        read_only_fields = ['uuid', 'creator', 'created_on']

    def create(self, validated_data):
        validated_data['uuid'] = create_uuid()
        validated_data['created_by'] = self.context.get('user')

        return super().create(validated_data)

    def to_representation(self, instance):
        """Warns about alcoholic drinks"""
        drink = super().to_representation(instance)
        if drink['name'].startswith('Al.'):
            drink['name'] = drink['name'].replace('Al.', 'Not for pregnant people,')
        return drink

    def get_name(self, obj):
        return 'Drink: ' + obj.name
