from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chatbot, ChatbotCustomization
from .serializers import ChatbotCustomizationSerializer
from .utils import bot_answer
from django.utils import timezone


class ChatbotCustomizationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ChatbotCustomizationSerializer
    permission_classes = []

    def get_queryset(self):
        return ChatbotCustomization.objects.filter(chatbot__user=1)

    def get_object(self):
        chatbot_id = self.kwargs['chatbot_id']
        return ChatbotCustomization.objects.get(chatbot__id=chatbot_id, chatbot__user=1)

class ValidateChatBotAPIView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')

        if not api_key:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        from chatbots.models import Chatbot
        try:
            bot = Chatbot.objects.get(api_key=api_key)
        except Chatbot.DoesNotExist:
            return Response({'error': 'Invalid API key'}, status=status.HTTP_403_FORBIDDEN)

        ui = ChatbotCustomization.objects.filter(chatbot=bot).first()
        if ui:
            ui = ChatbotCustomizationSerializer(ui).data
        return Response({'name': bot.name, 'ui': ui}, status=status.HTTP_200_OK)

class ChatBotAnswerAPIView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key')
        query = request.data.get('query', '').strip()

        if not api_key or not query:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bot = Chatbot.objects.get(api_key=api_key)
            if not bot.is_active:
                return Response({'error': 'Inactive'}, status=status.HTTP_400_BAD_REQUEST)
        except Chatbot.DoesNotExist:
            return Response({'error': 'Invalid API key'}, status=status.HTTP_403_FORBIDDEN)

        reply_list = bot_answer(bot.name, query)
        reply = ''
        for r in reply_list:
            reply += r['result']

        bot.last_used = timezone.now()
        bot.messages += 1
        bot.save()
        return Response({'reply': reply}, status=status.HTTP_200_OK)
