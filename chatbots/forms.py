from django import forms
from .models import Chatbot
from subscriptions.models import UserSubscription
from django.utils.timezone import now


class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
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

        if not self.request or self.request.user.is_superuser:
            return cleaned_data
        
        self.instance.user = self.request.user

        if self.instance.pk is None:
            user = self.request.user
            subscription =  cleaned_data['subscription']
            user_chat_bots = Chatbot.objects.filter(user=user, subscription=subscription).count()
            
            if user_chat_bots >= subscription.plan.max_chatbots:
                raise forms.ValidationError(
                    f"You have reached the maximum number of chatbots allowed with the selected subscription ({subscription.plan.max_chatbots})."
                )
        print("Cleaned data:", cleaned_data)
        return cleaned_data
