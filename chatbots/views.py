from rest_framework import generics, permissions
from .models import Chatbot, ChatbotCustomization
from .serializers import ChatbotCustomizationSerializer


class ChatbotCustomizationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ChatbotCustomizationSerializer
    permission_classes = []

    def get_queryset(self):
        return ChatbotCustomization.objects.filter(chatbot__user=1)

    def get_object(self):
        chatbot_id = self.kwargs['chatbot_id']
        return ChatbotCustomization.objects.get(chatbot__id=chatbot_id, chatbot__user=1)