from django.urls import path
from .views import GoogleLoginAPIView, LoginAPIView, RegisterAPIView


urlpatterns = [
    path('google-login/', GoogleLoginAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
]
