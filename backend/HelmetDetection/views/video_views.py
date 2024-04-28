from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from HelmetDetection.apps import HelmetdetectionConfig as HD

__all__ = ['upload_video', 'detect_video']


@csrf_exempt
def upload_video(request: HttpRequest):
    if request.method == 'POST':
        vid = request.FILES.get('video')

        vid_path = 'media/' + vid.name
        with open(vid_path, 'wb') as f:
            for chunk in vid.chunks():
                f.write(chunk)
        
        vid_url = request.build_absolute_uri(vid_path)

        return JsonResponse({'video_url': vid_url})
    else:
        return JsonResponse({'error': 'No video file provided'}, status=405)
    

def detect_video(request: HttpRequest):
    y5d = HD.y5d

    video_name = request.GET.get('video_name')
    vid_path = 'media/' + video_name

    save_path = y5d.detect_and_save_video(vid_path)
    detect_video_url = request.build_absolute_uri(save_path)

    return JsonResponse({'detected_path': detect_video_url})
