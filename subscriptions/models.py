from django.db import models
from accounts.models import User


class Subscription(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_month = models.PositiveIntegerField(default=0)
    is_free_trial = models.BooleanField(default=False)
    days = models.PositiveIntegerField(default=0)
    max_chatbots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subscription.name

class PaymentTransaction(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    method = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_subscription.subscription.name
