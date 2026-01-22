from django.contrib import admin
from .models import MobileOTP


@admin.register(MobileOTP)
class MobileOTPAdmin(admin.ModelAdmin):
    list_display = (
        "mobile",
        "otp",
        "resend_count",
        "attempt_count",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("mobile",)
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)
