from rest_framework import serializers
from django.contrib.auth.models import User

from HelmetDetection.models import Image, Video
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='userprofile.gender', max_length=5, required=False)
    age = serializers.IntegerField(source='userprofile.age', required=False)
    phone_number = serializers.CharField(source='userprofile.phone_number', max_length=15, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'gender', 'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)

        profile_data = validated_data.pop('userprofile', {})

        user = User.objects.create_user(
            **validated_data
        )
        UserProfile.objects.create(
            user=user, 
            **profile_data
        )
        return user
    

class UserUploadSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())
    videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'images', 'videos')


class UserInfoSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='userprofile.gender', max_length=5, required=False)
    age = serializers.IntegerField(source='userprofile.age', required=False)
    phone_number = serializers.CharField(source='userprofile.phone_number', max_length=15, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'gender', 'age', 'phone_number')
