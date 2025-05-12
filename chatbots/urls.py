from django.urls import path
from .views import ChatbotCustomizationDetailView


urlpatterns = [
    path('chatbot/<int:chatbot_id>/customization/', ChatbotCustomizationDetailView.as_view(), name='chatbot-customization'),
]
