from users.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField("get_username")
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    # def get_username(self, obj):
    #     print(obj.username)
    #     return 'noe' + obj.username
