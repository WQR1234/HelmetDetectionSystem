from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from HelmetDetection.apps import HelmetdetectionConfig as HD
from HelmetDetection.serializers import ImageSerializer

import os

# Create your views here.

__all__ = ['upload_image', 'detect_image', 'download_image']

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         img = request.FILES.get('image')

#         img_url = 'media/'+img.name
#         with open(img_url, 'wb') as f:
#             for chunk in img.chunks():
#                 f.write(chunk)
        
#         img_url = request.build_absolute_uri(img_url)
        
#         return JsonResponse({'image_url': img_url})
#     else:
#         return JsonResponse({'error': 'No image file provided'}, status=400)
    

@api_view(['POST'])
def upload_image(request: HttpRequest):
    if request.method == 'POST':
        img = request.FILES.get('image')
        user = request.user
        if not user.username:
            img_url = 'media/'+img.name
            with open(img_url, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            
            img_url = request.build_absolute_uri(img_url)
            
            return JsonResponse({'image_url': img_url})
        else:
            img_url = f'media/{user.id}-{img.name}'
            with open(img_url, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            
            img_url = request.build_absolute_uri(img_url)
            image_data = {
                'user': user.id,
                'image_url': img_url
            }
            serializer = ImageSerializer(data=image_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

def detect_image(request):
    y5d = HD.y5d
    # print(type(y5d), type(y5d.model))
    image_name = request.GET.get('image_name')


    # image_dir = os.path.dirname(image_path)
    pure_name, image_extension = os.path.splitext(image_name)

    save_path = 'media/'+pure_name+'-detected'+image_extension

    image_name = 'media/'+image_name
    if not os.path.exists(save_path):  
        y5d.detect_and_save_image(image_name, save_path)

    detected_image_url = request.build_absolute_uri(save_path)
    
    return JsonResponse({'detected_path': detected_image_url})


def download_image(request):
    image_name = request.GET.get('image_name')
    print(image_name)

    with open('media/'+image_name, 'rb') as f:
        response = HttpResponse(f.read())
        response['Content-Type'] = 'image/*'
        response['Content-Disposition'] = 'attachment;filename=' + image_name
        
    return response