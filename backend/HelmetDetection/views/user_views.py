from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import json

__all__ = ['register_user', 'login_user', 'check_login']


@csrf_exempt
def register_user(request: HttpRequest):
    if request.method == 'POST':

        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        # print(username, password)
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        # Create a new user
        user = User.objects.create_user(username, password=password)
        user.save()
        
        return JsonResponse({'message': 'User registered successfully'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login_user(request: HttpRequest):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def check_login(request: HttpRequest):
    print(request.user.username)

    if request.user.username:
        
        return JsonResponse({'isLogin': True})
    return JsonResponse({'isLogin': False})


