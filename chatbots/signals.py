from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chatbot
from .utils import process_chatbot


@receiver(post_save, sender=Chatbot)
def handle_new_chatbot(sender, instance, created, **kwargs):
    if created:
        process_chatbot.delay(instance.id)
