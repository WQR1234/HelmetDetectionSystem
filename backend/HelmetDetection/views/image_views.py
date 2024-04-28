from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from HelmetDetection.apps import HelmetdetectionConfig as HD

# Create your views here.

__all__ = ['upload_image', 'detect_image', 'download_image']

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        img = request.FILES.get('image')

        img_url = 'media/'+img.name
        with open(img_url, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        
        img_url = request.build_absolute_uri(img_url)
        
        return JsonResponse({'image_url': img_url})
    else:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    

def detect_image(request):
    y5d = HD.y5d
    # print(type(y5d), type(y5d.model))
    image_name = request.GET.get('image_name')
    image_name = 'media/'+image_name
    save_path = y5d.detect_and_save_image(image_name)
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