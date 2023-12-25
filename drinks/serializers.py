from rest_framework import serializers

from .models import Drink, DrinkImage
from .helpers import create_uuid


class DrinkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrinkImage
        fields = '__all__'


class DrinkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    creator = serializers.CharField(source='created_by.username', read_only=True)

    images = DrinkImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=False),
                                            write_only=True)

    class Meta:
        model = Drink
        fields = ['uuid', 'name', 'description', 'price', 'is_publishable', 'creator', 'created_on', "images",
                  "uploaded_images"]
        read_only_fields = ['uuid', 'creator', 'created_on']

    def create(self, validated_data):
        validated_data['uuid'] = create_uuid()
        validated_data['created_by'] = self.context.get('user')

        uploaded_images = validated_data.pop("uploaded_images")
        drink = Drink.objects.create(**validated_data)
        print(validated_data)

        for image in uploaded_images:
            DrinkImage.objects.create(drink=drink, image=image)

        # return super().create(validated_data)
        return drink

    def to_representation(self, instance):
        """Warns about alcoholic drinks"""
        drink = super().to_representation(instance)
        if drink['name'].startswith('Al.'):
            drink['name'] = drink['name'].replace('Al.', 'Not for pregnant people,')
        return drink

    def get_name(self, obj):
        return 'Drink: ' + obj.name