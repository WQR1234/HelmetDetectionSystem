from rest_framework import serializers
from .models import Image, Video

class ImageSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'user', 'image_name', 'image_path']

    def get_image_path(self, obj):
        return f'media/images/{obj.user.id}/origin/{obj.image_name}'


class VideoSerializer(serializers.ModelSerializer):
    video_path = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'user', 'video_name', 'video_path']

    def get_video_path(self, obj):
        return f'media/videos/{obj.user.id}/origin/{obj.video_name}'