from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Chatbot
from .utils import process_chatbot
import os
from django.conf import settings
import shutil


@receiver(post_save, sender=Chatbot)
def handle_new_chatbot(sender, instance, created, **kwargs):
    if created:
        process_chatbot.delay(instance.id)

@receiver(post_delete, sender=Chatbot)
def handle_deleted_chatbot(sender, instance, **kwargs):
    vector_store_path = os.path.join(settings.CHROMA_STORE_DIR, instance.name)
    if os.path.exists(vector_store_path):
        shutil.rmtree(vector_store_path)
