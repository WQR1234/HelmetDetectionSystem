from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .apps import HelmetdetectionConfig as HD

# Create your views here.


def foobar(request):
    y5d = HD.y5d
    print(type(y5d), type(y5d.model))
    
    return JsonResponse({'foo': 1, 'bar': 'a'})


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