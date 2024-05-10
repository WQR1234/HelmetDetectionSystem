import cv2
from django.http import StreamingHttpResponse, JsonResponse

from HelmetDetection.apps import HelmetdetectionConfig as HD

__all__ = ['stream_camera', 'check_camera']

def stream_camera(request):
    cap = cv2.VideoCapture(0)
    y5d = HD.y5d

    def generate():
        while True:
            ret, frame = cap.read()
            frame = y5d.detect_and_save_image(frame, None, False)
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

def check_camera(request):
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        return JsonResponse({'camera_open': True})
    return JsonResponse({'camera_open': False})