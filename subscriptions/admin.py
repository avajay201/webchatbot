from django.contrib import admin
from .models import MembershipPlan, UserSubscription, PaymentTransaction
from unfold.admin import ModelAdmin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import MembershipPlan
from django.urls import path


@admin.register(MembershipPlan)
class MembershipPlanAdmin(ModelAdmin):
    change_form_template = "admin/subscriptions/membershipplan/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:membership_id>/purchase/",
                self.admin_site.admin_view(self.purchase_membership),
                name="purchase_membership",
            ),
        ]
        return custom_urls + urls

    def purchase_membership(self, request, membership_id):
        messages.success(request, _("Membership Plan purchased successfully."))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))

@admin.register(UserSubscription)
class UserSubscriptionAdmin(ModelAdmin):
    pass

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    pass

