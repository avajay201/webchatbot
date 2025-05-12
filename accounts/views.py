from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User


class GoogleLoginAPIView(APIView):
    """
    Authenticate or register a user via Google OAuth token.

    Expected POST data:
    - token: Google ID token obtained from frontend

    On success:
    - Creates a new user if not exists
    - Returns access and refresh JWT tokens
    - Returns basic user info
    """
    def post(self, request):
        token = request.data.get('token', '').strip()
        if not token:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(token, Request(), settings.GOOGLE_CLIENT_ID)
            user, created = User.objects.get_or_create(email=idinfo['email'])
            if created:
                user.username = idinfo.get('name', 'default_username')
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        except Exception as err:
            print('Google login error:', err)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPIView(APIView):
    """
    Authenticate a user using email and password.

    Expected POST data:
    - email: User's email
    - password: User's password

    On success:
    - Returns access and refresh JWT tokens
    - Returns basic user info
    """
    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    """
    Register a new user using email and password.

    Expected POST data:
    - fname: First name
    - lname: Last name
    - email: Email address
    - password: Password

    On success:
    - Creates new user
    - Returns access and refresh JWT tokens
    - Returns basic user info
    """
    def post(self, request):
        fname = request.data.get('fname', '').strip()
        lname = request.data.get('lname', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password')
        if not fname or not lname or not email or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            return Response({'error': 'User already registered with this email, please try different one.'}, status=status.HTTP_400_BAD_REQUEST)

        username = email.split('@')[0]
        user = User.objects.create(first_name=fname, last_name=lname, username=username, email=email)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
