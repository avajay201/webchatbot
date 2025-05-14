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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget


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
        if subscription.is_free_trial and not subscription.price:
            user_subscription = UserSubscription.objects.filter(user=request.user, subscription=subscription).first()
            if user_subscription:
                messages.info(request, _("Looks like you've already purchased this subscription."))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/dashboard/"))

            end_date = datetime.now() + relativedelta(days=subscription.days)
            UserSubscription.objects.create(
                user=request.user,
                subscription=subscription,
                end_date = end_date
            )
            messages.success(request, _("Subscription purchased successfully."))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/dashboard/"))
        else:
            user_subscription = UserSubscription.objects.filter(user=request.user, subscription=subscription).first()
            if user_subscription.end_date >= timezone.now():
                messages.info(request, _("You already have an active subscription to this plan."))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/dashboard/"))

        payment_url = self.get_payment_url(request.user, subscription)
        print('Subscription purchase payment URL:', payment_url)
        if not payment_url:
            messages.error(request, _("Failed to purchase this subscription."))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/dashboard/"))
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


admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)

class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass

class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()

@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm

@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass

@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass

@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass

@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass
