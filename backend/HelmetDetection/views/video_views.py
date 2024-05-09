import os

from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from HelmetDetection.apps import HelmetdetectionConfig as HD
from HelmetDetection.serializers import VideoSerializer

__all__ = ['upload_video', 'detect_video']


@api_view(['POST'])
def upload_video(request: HttpRequest):
    if request.method == 'POST':
        vid = request.FILES.get('video')

        user = request.user
        if not user.username:
            vid_path = 'media/videos/origin/'+vid.name
            if os.path.exists(vid_path):
                vid_path += '_'
            with open(vid_path, 'wb') as f:
                for chunk in vid.chunks():
                    f.write(chunk)
            
            return JsonResponse({'video_path': vid_path})
        else:
            vid_path = f'media/videos/{user.id}/origin/{vid.name}'
            with open(vid_path, 'wb') as f:
                for chunk in vid.chunks():
                    f.write(chunk)
            
            video_data = {
                'user': user.id,
                'video_name': vid.name
            }
            serializer = VideoSerializer(data=video_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def detect_video(request: HttpRequest):
    y5d = HD.y5d

    video_name = request.GET.get('video_name')
    user = request.user
    if user.username:
        save_path = f'media/videos/{user.id}/detected/{video_name}'
        video_path = f'media/videos/{user.id}/origin/{video_name}'
        
    else:
        save_path = f'media/videos/detected/{video_name}'
        video_path = f'media/videos/origin/{video_name}'

    if not os.path.exists(save_path):  
        y5d.detect_and_save_video(video_path, save_path)
    
    return JsonResponse({'detected_path': save_path})
