from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from HelmetDetection.serializers import ImageSerializer

# Create your views here.


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    # print(user.images.all())
    user_info = {
        'id': user.id,
        'username': user.username,
        # 其他用户信息
    }
    return Response(user_info, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    user = request.user
    images = user.images.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)