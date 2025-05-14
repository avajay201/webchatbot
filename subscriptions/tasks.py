from celery import shared_task
from django.utils import timezone
from .models import UserSubscription


@shared_task
def deactivate_expired_subscriptions():
    print("***Running deactivate_expired_subscriptions***")
    now = timezone.now()
    count = UserSubscription.objects.filter(end_date__lt=now, is_active=True).update(is_active=False)
    return f"{count} expired subscriptions deactivated"
