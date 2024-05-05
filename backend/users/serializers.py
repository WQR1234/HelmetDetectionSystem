from rest_framework import serializers
from django.contrib.auth.models import User

from HelmetDetection.models import Image


class UserSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'images')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user