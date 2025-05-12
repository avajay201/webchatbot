from rest_framework import serializers
from .models import ChatbotCustomization


class ChatbotCustomizationSerializer(serializers.ModelSerializer):
    bot_name = serializers.CharField(source='chatbot.name', read_only=False)

    class Meta:
        model = ChatbotCustomization
        fields = '__all__'
        read_only_fields = ['chatbot']

    def update(self, instance, validated_data):
        chatbot_data = validated_data.pop('chatbot', {})
        bot_name = chatbot_data.get('name')

        if bot_name:
            chatbot = instance.chatbot
            chatbot.name = bot_name
            chatbot.save()

        return super().update(instance, validated_data)