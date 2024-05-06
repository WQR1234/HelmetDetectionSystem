from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from HelmetDetection.apps import HelmetdetectionConfig as HD
from HelmetDetection.serializers import ImageSerializer

import os

# Create your views here.

__all__ = ['upload_image', 'detect_image']

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
            img_path = 'media/images/origin/'+img.name
            with open(img_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            
            return JsonResponse({'image_path': img_path})
        else:
            img_path = f'media/images/{user.id}/origin/{img.name}'
            with open(img_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            
            image_data = {
                'user': user.id,
                'image_name': img.name
            }
            serializer = ImageSerializer(data=image_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def detect_image(request: HttpRequest):
    y5d = HD.y5d
    # print(type(y5d), type(y5d.model))
    image_name = request.GET.get('image_name')
    user = request.user
    if user.username:
        save_path = f'media/images/{user.id}/detected/{image_name}'
        image_path = f'media/images/{user.id}/origin/{image_name}'
        
    else:
        save_path = f'media/images/detected/{image_name}'
        image_path = f'media/images/origin/{image_name}'

    if not os.path.exists(save_path):  
        y5d.detect_and_save_image(image_path, save_path)
    
    return JsonResponse({'detected_path': save_path})

