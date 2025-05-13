from django.db import models
from accounts.models import User
from colorfield.fields import ColorField
from subscriptions.models import UserSubscription
from django.core.validators import MaxValueValidator, MinValueValidator


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
    border_radius = models.PositiveSmallIntegerField(
        default=16,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        help_text="Chat Bot border radius in pixels (between 0 and 25)"
    )
    welcome_message = models.CharField(max_length=255, default="Hi there! How can I help you?")
    input_placeholder_text = models.CharField(max_length=255, default="Type your message...")
    scrollbar_width = models.PositiveSmallIntegerField(
        default=6,
        validators=[MinValueValidator(4), MaxValueValidator(12)],
        help_text="Scrollbar width in pixels (between 4 and 12)"
    )

    # Colors
    chat_icon_bg_color = models.CharField(max_length=7, default="#4a6cf7")
    chat_icon_color = models.CharField(max_length=7, default="#ffffff")
    chat_close_btn_color = models.CharField(max_length=7, default="#ffffff")
    header_bg_color = models.CharField(max_length=7, default="#0d0a0a")
    header_text_color = models.CharField(max_length=7, default="#ffffff")
    msg_box_bg_color = models.CharField(max_length=7, default="#ffbac6")
    scrollbar_color = models.CharField(max_length=7, default="#ffbac6")
    send_btn_color = models.CharField(max_length=7, default="#000000")
    user_message_bg_color = models.CharField(max_length=7, default="#171b2b")
    user_message_text_color = models.CharField(max_length=7, default="#ffffff")
    bot_message_bg_color = models.CharField(max_length=7, default="#573b40")
    bot_message_text_color = models.CharField(max_length=7, default="#ffffff")
    input_container_bg_color = models.CharField(max_length=7, default="#ffffff")
    input_color = models.CharField(max_length=7, default="#000000")
    input_border_color = models.CharField(max_length=7, default="#b9b4b4")
    input_placeholder_color = models.CharField(max_length=7, default="#808080")

    def __str__(self):
        return self.chatbot.name
