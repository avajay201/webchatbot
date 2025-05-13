from django.urls import path
from .views import razorpay_callback


urlpatterns = [
    path('callback/', razorpay_callback, name='razorpay_callback'),
]
