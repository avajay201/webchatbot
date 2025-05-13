from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
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

    if not payment_id or not payment_link_id:
        return HttpResponseBadRequest("Invalid request")

    try:
        payment_info = client.payment.fetch(payment_id)

        user_id = payment_info.get("notes", {}).get("user_id")
        sub_id = payment_info.get("notes", {}).get("sub_id")
        
        if not user_id or not sub_id:
            return HttpResponseBadRequest("Invalid request")

        user = User.objects.filter(id=user_id).first()

        if not user:
            return HttpResponseBadRequest("Invalid request")

        amount = Decimal(payment_info['amount']) / 100
        
        subscription = Subscription.objects.get(id=sub_id)
        end_date = datetime.now() + relativedelta(months=subscription.duration_month)

        user_subscription = UserSubscription.objects.create(
            user=user,
            subscription=subscription,
            end_date=end_date
        )
        PaymentTransaction.objects.create(
            user_subscription=user_subscription,
            amount=amount,
            payment_id=payment_info['id'],
            contact=payment_info['contact'],
            method=payment_info['method'],
            status='completed' if payment_info['status'] == 'captured' else 'failed',
        )

        return JsonResponse({'message': 'Payment recorded successfully'})
    except Exception as e:
        print('Payment status capturing error:', e)
        return JsonResponse({'error': 'Something went wrong'}, status=400)
