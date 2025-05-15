from rest_framework import serializers
from .models import ChatbotCustomization


class ChatbotCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotCustomization
        exclude = ('chatbot', 'id')
