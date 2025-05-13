from django.contrib import admin
from .models import Subscription, UserSubscription, PaymentTransaction
from unfold.admin import ModelAdmin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Subscription
from django.urls import path
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_ID))

@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    change_form_template = "admin/subscriptions/subscription/change_form.html"

    def get_payment_url(self, user, subscription):
        amount = int(subscription.price)
        try:
            payment_link = client.payment_link.create({
                "amount": amount * 100,
                "currency": "INR",
                "description": f"Subscription: {subscription.name}({subscription.duration_month} month)",
                "customer": {
                    "name": f'{user.first_name} {user.last_name}'.strip() or user.username,
                    "email": user.email,
                },
                "notify": {
                    "sms": True,
                    "email": True,
                },
                "callback_url": f"{settings.BASE_URL}/payment/callback/",
                "callback_method": "get",
                "notes": {
                    "user_id": user.id,
                    "sub_id": subscription.id
                }
            })

            return payment_link['short_url']
        except Exception as e:
            print('Payment URL creating error:', e)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:subscription_id>/purchase/",
                self.admin_site.admin_view(self.purchase_subscription),
                name="purchase_subscription",
            ),
        ]
        return custom_urls + urls

    def purchase_subscription(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, pk=subscription_id)
        payment_url = self.get_payment_url(request.user, subscription)
        print('Subscription purchase payment URL:', payment_url)
        if not payment_url:
            messages.error(request, _("Failed to purchase this subscription."))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))
        return redirect(payment_url)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            return [field for field in fields if field not in ['user']]
        return fields

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    pass
