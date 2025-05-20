from django import forms
from .models import Chatbot, ChatbotCustomization
from subscriptions.models import UserSubscription
from django.utils.timezone import now
from .utils import is_reachable_url


class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if 'subscription' in list(self.fields.keys()):
            if self.request and not self.request.user.is_superuser:
                self.fields['subscription'].queryset = UserSubscription.objects.filter(
                    user=self.request.user,
                    is_active=True,
                    end_date__gte=now()
                )
            elif 'subscription' in self.fields:
                self.fields['subscription'].queryset = UserSubscription.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        data_fields = list(cleaned_data.keys())

        if not self.request or self.request.user.is_superuser:
            return cleaned_data

        self.instance.user = self.request.user

        if self.instance.pk is None and 'subscription' in data_fields:
            user = self.request.user
            subscription =  cleaned_data['subscription']
            user_chat_bots = Chatbot.objects.filter(
                user=user,
                subscription=subscription,
                status__in=['success', 'in_progress']
            ).count()

            if user_chat_bots >= subscription.subscription.max_chatbots:
                raise forms.ValidationError(
                    f"You have reached the maximum number of chatbots allowed with the selected subscription ({subscription.subscription.max_chatbots})."
                )

        if 'website_url' in data_fields:
            web_url = cleaned_data['website_url']
            is_reachable = is_reachable_url(web_url)
            if not is_reachable:
                raise forms.ValidationError(
                    f"This website URL is unreachable."
                )

        if Chatbot.objects.exclude(pk=self.instance.pk).filter(name=cleaned_data['name'], status__in=['in_progress', 'success']).exists():
            raise forms.ValidationError("Chatbot with this name already exists and is active or in progress.")

        if 'website_url' in data_fields:
            if Chatbot.objects.exclude(pk=self.instance.pk).filter(website_url=cleaned_data['website_url'], status__in=['in_progress', 'success']).exists():
                raise forms.ValidationError("Chatbot with this website URL already exists and is active or in progress.")

        if self.instance.status != 'success':
            self.instance.status = 'in_progress'
        return cleaned_data

class ChatbotCustomizationForm(forms.ModelForm):
    class Meta:
        model = ChatbotCustomization
        fields = '__all__'

        color_fields = [
            'chat_icon_bg_color',
            'chat_icon_color',
            'chat_close_btn_color',
            'header_bg_color',
            'header_text_color',
            'msg_box_bg_color',
            'scrollbar_color',
            'send_btn_color',
            'user_message_bg_color',
            'user_message_text_color',
            'bot_message_bg_color',
            'bot_message_text_color',
            'input_container_bg_color',
            'input_color',
            'input_border_color',
            'input_placeholder_color',
        ]

        number_fields = {
            'border_radius': forms.NumberInput(attrs={
                'min': 0,
                'max': 25,
                'step': 1,
                'class': 'border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark group-[.primary]:border-transparent px-3 py-2 w-full max-w-2xl'
            }),
            'scrollbar_width': forms.NumberInput(attrs={
                'min': 4,
                'max': 12,
                'step': 1,
                'class': 'border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark group-[.primary]:border-transparent px-3 py-2 w-full max-w-2xl'
            }),
        }

        widgets = {
            **{
                field: forms.TextInput(attrs={'type': 'color', 'style': 'width: 70px; height: 35px;'})
                for field in color_fields
            },
            **number_fields
        }
