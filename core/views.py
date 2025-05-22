from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import timedelta
from django.utils import timezone
from chatbots.models import Chatbot
from subscriptions.models import UserSubscription
from django.db.models import Sum


def dashboard_callback(request, context):
    if not request.user.is_superuser:
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        one_month_ago = now - timedelta(days=30)
        
        # 1. Chatbots data
        active_chatbots = Chatbot.objects.filter(user=request.user, is_active=True, created_at__gte=three_months_ago)
        chatbots_created_last_month = active_chatbots.filter(created_at__gte=one_month_ago).count()

        # 2. Memberships (UserSubscription) data
        active_memberships = UserSubscription.objects.filter(user=request.user, is_active=True, start_date__gte=three_months_ago)
        memberships_purchased_last_month = active_memberships.filter(start_date__gte=one_month_ago).count()

        # 3. Latest chatbot
        latest_chatbot = Chatbot.objects.filter(user=request.user).order_by('-created_at').first()

        # 4. Memberships expiring soon (within 7 days)
        expiring_soon = UserSubscription.objects.filter(
            user=request.user,
            is_active=True,
            end_date__lte=now + timedelta(days=7)
        ).first()
        
        # 5. All chatbots
        chatbots = Chatbot.objects.filter(user=request.user)

        # 5. All subscriptions
        subscriptions = UserSubscription.objects.filter(user=request.user)
        for sub in subscriptions:
            sub.chatbot_count = Chatbot.objects.filter(subscription=sub).count()

        context.update({
            "tabs": ["Overview", "Chatbots", "Subscriptions"],
            "current_tab": request.session.get('current_tab', 'overview'),
            "active_chatbots": active_chatbots.count(),
            "chatbots_created_last_month": chatbots_created_last_month,
            "active_memberships": active_memberships.count(),
            "memberships_purchased_last_month": memberships_purchased_last_month,
            "total_messages": chatbots.aggregate(total=Sum('messages'))['total'] or 0,
            "total_messages_last_month": chatbots.filter(created_at__gte=one_month_ago).aggregate(total=Sum('messages'))['total'] or 0,
            "latest_chatbot": latest_chatbot,
            "expiring_soon": expiring_soon,
            "chatbots": chatbots,
            "subscriptions": subscriptions,
        })

    return context

@csrf_exempt
def set_tab_session(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tab = data.get("tab")
        request.session["current_tab"] = tab
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "invalid method"}, status=405)
