from django.urls import path
from .views import ChatbotCustomizationDetailView, ValidateChatBotAPIView, ChatBotAnswerAPIView


urlpatterns = [
    path('chatbot/<int:chatbot_id>/customization/', ChatbotCustomizationDetailView.as_view(), name='chatbot-customization'),
    path('validate-chatbot/', ValidateChatBotAPIView.as_view(), name='validate-chatbot'),
    path('chatbot-reply/', ChatBotAnswerAPIView.as_view(), name='chatbot-reply'),
]
