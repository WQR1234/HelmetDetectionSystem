import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .serializers import UserRegisterSerializer, UserInfoSerializer
from HelmetDetection.serializers import ImageSerializer, VideoSerializer
from HelmetDetection.models import Image, Video

from datetime import datetime, date

# Create your views here.


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            os.mkdir(f"media/images/{serializer.data['id']}")
            os.mkdir(f"media/videos/{serializer.data['id']}")
            os.mkdir(f"media/images/{serializer.data['id']}/origin")
            os.mkdir(f"media/videos/{serializer.data['id']}/origin")
            os.mkdir(f"media/images/{serializer.data['id']}/detected")
            os.mkdir(f"media/videos/{serializer.data['id']}/detected")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    # print(user.images.all())
    query = User.objects.get(id=user.id)
    serializer = UserInfoSerializer(query)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    images = user.images.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_videos(request):
    user = request.user
    images = user.videos.all()
    serializer = VideoSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request, image_id):
    user = request.user
    try:
        image = Image.objects.get(user=user, id=image_id)
    except Image.DoesNotExist:
        return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    
    image.delete()
    return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_video(request, video_id):
    user = request.user
    try:
        video = Video.objects.get(user=user, id=video_id)
    except Video.DoesNotExist:
        return Response({"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    
    video.delete()
    return Response({"message": "Video deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_images_in_date_range(request):
    user = request.user

    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')

    if not start_date_str:
        start_date = date(2000, 1, 1)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    if not end_date_str:
        end_date = date(2099, 12, 31)
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    images = Image.objects.filter(user=user, upload_date__range=[start_date, end_date])
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_videos_in_date_range(request):
    user = request.user

    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')

    if not start_date_str:
        start_date = date(2000, 1, 1)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    if not end_date_str:
        end_date = date(2099, 12, 31)
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    images = Video.objects.filter(user=user, upload_date__range=[start_date, end_date])
    serializer = VideoSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
