from django.db import models
from accounts.models import User


class MembershipPlan(models.Model):
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
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    trial_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class PaymentTransaction(models.Model):
    subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True)
    payment_gateway = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("success", "Success"), ("failed", "Failed")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.plan.name}"
