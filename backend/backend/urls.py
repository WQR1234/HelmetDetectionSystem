"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRegisterAPIView, get_user_info, get_user_images, get_user_videos, delete_image, delete_video, \
                                            get_images_in_date_range, get_videos_in_date_range
from HelmetDetection import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 图片相关url
    path('upload_image/', views.upload_image), 
    path('detect_image/', views.detect_image),

    # 视频相关url
    path('upload_video/', views.upload_video), 
    path('detect_video/', views.detect_video),

    # 用户相关url
    # path('register/', views.register_user),
    # path('login/', views.login_user),
    # path('check_login/', views.check_login),

    path('register/', UserRegisterAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('check_login/', get_user_info),
    path('get_images/', get_user_images),
    path('get_videos/', get_user_videos),
    path('delete_image/<int:image_id>/', delete_image),
    path('delete_video/<int:video_id>/', delete_video),

    path('get_images_by_date/', get_images_in_date_range), 
    path('get_videos_by_date/', get_videos_in_date_range), 

    path('check_camera/', views.check_camera),

    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, 'media')

]
