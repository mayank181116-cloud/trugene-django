from django.db import models
from django.utils import timezone
from django.conf import settings


class MobileOTP(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    resend_count = models.PositiveIntegerField(default=0)
    attempt_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiry_seconds = getattr(settings, "OTP_EXPIRY_SECONDS", 300)
        return (timezone.now() - self.created_at).total_seconds() > expiry_seconds

    def __str__(self):
        return f"{self.mobile} | OTP:{self.otp}"
