from django.contrib import admin
from .models import Chatbot, ChatbotCustomization
from unfold.admin import ModelAdmin
from .forms import ChatbotForm, ChatbotCustomizationForm


@admin.register(Chatbot)
class ChatbotAdmin(ModelAdmin):
    readonly_fields = ('api_key', 'sdk', 'status', 'created_at', 'updated_at')
    form = ChatbotForm
    
    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return Form(*args, **kwargs)
        return RequestForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            return [field for field in fields if field not in ['user']]
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('website_url',) + self.readonly_fields
        return self.readonly_fields

@admin.register(ChatbotCustomization)
class ChatbotCustomizationAdmin(ModelAdmin):
    form = ChatbotCustomizationForm
    change_form_template = "admin/chatbots/chatbotcustomization/change_form.html"

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'chatbot' in fields:
            fields.remove('chatbot')
        return ['chatbot'] + fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('chatbot',) + self.readonly_fields
        return self.readonly_fields
