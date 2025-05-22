from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from subscriptions.models import Subscription, UserSubscription, PaymentTransaction
from accounts.models import User
import razorpay
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_ID))

@csrf_exempt
def razorpay_callback(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request")

    payment_id = request.GET.get('razorpay_payment_id')
    payment_link_id = request.GET.get('razorpay_payment_link_id')
    redirect_url = request.GET.get('next') or "/dashboard/"

    if not payment_id or not payment_link_id:
        return redirect(f"{redirect_url}?status=error")

    try:
        payment_info = client.payment.fetch(payment_id)

        user_id = payment_info.get("notes", {}).get("user_id")
        sub_id = payment_info.get("notes", {}).get("sub_id")

        if not user_id or not sub_id:
            return redirect(f"{redirect_url}?status=error")

        user = User.objects.filter(id=user_id).first()
        subscription = Subscription.objects.get(id=sub_id)

        if not user:
            return redirect(f"{redirect_url}?status=error")

        amount = Decimal(payment_info['amount']) / 100

        transaction = PaymentTransaction.objects.create(
            user=user,
            subscription=subscription,
            amount=amount,
            payment_id=payment_info['id'],
            contact=payment_info['contact'],
            method=payment_info['method'],
            status='completed' if payment_info['status'] == 'captured' else 'failed',
        )

        if transaction.status == 'completed':
            end_date = datetime.now() + relativedelta(months=subscription.duration_month)

            user_subscription = UserSubscription.objects.filter(user=user, subscription=subscription).first()
            if user_subscription:
                user_subscription.renew()
            else:
                user_subscription = UserSubscription.objects.create(
                    user=user,
                    subscription=subscription,
                    end_date=end_date
                )
            return redirect(f"{redirect_url}usersubscription/{user_subscription.id}/change/?status=success")
        return redirect(f"{redirect_url}usersubscription/{user_subscription.id}/change/?status=error")
    except Exception as e:
        print('Payment status capturing error:', e)
        return redirect(f"{redirect_url}subscription/{subscription.id}/change/?status=error")
