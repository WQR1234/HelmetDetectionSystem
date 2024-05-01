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


from HelmetDetection import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 图片相关url
    path('upload_image/', views.upload_image), 
    path('detect_image/', views.detect_image),
    path('download_image/', views.download_image), 

    # 视频相关url
    path('upload_video/', views.upload_video), 
    path('detect_video/', views.detect_video),

    # 用户相关url
    # path('register/', views.register_user),
    # path('login/', views.login_user),
    # path('check_login/', views.check_login),

    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, 'media')

]
