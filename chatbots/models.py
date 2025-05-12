from django.db import models
from accounts.models import User
from colorfield.fields import ColorField
from subscriptions.models import UserSubscription


class Chatbot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    website_url = models.URLField(unique=True)
    api_key = models.CharField(max_length=150, unique=True)
    sdk = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ChatbotCustomization(models.Model):
    FONT_CHOICES = [
        ("Arial, sans-serif", "Arial"),
        ("'Helvetica Neue', sans-serif", "Helvetica Neue"),
        ("'Times New Roman', serif", "Times New Roman"),
        ("'Courier New', monospace", "Courier New"),
        ("'Georgia', serif", "Georgia"),
        ("'Tahoma', sans-serif", "Tahoma"),
        ("'Verdana', sans-serif", "Verdana"),
    ]

    chatbot = models.OneToOneField(Chatbot, on_delete=models.CASCADE, related_name='customization')

    # Layout
    font_family = models.CharField(max_length=100, choices=FONT_CHOICES, default="Arial, sans-serif")
    border_radius = models.PositiveSmallIntegerField(default=16, help_text="In pixels")
    welcome_message = models.CharField(max_length=255, default="Hi there! How can I help you?")
    chat_icon = models.ImageField(upload_to='chat_icons/', null=True, blank=True)

    # Colors
    header_bg_color = ColorField(default="#2563EB")
    header_text_color = ColorField(default="#2563EB")
    msg_box_bg_color = ColorField(default="#F43F5E")
    btn_color = ColorField(default="#F43F5E")
    user_message_bg_color = ColorField(default="#2563EB")
    user_message_text_color = ColorField(default="#2563EB")
    bot_message_bg_color = ColorField(default="#F43F5E")
    bot_message_text_color = ColorField(default="#F43F5E")

    def __str__(self):
        return self.chatbot.name
