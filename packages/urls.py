from django.urls import path
from . import views

app_name = "packages"

urlpatterns = [
    # 📦 Packages list
    path("", views.package_list, name="package_list"),

    # 📦 Book package
    path("book/<int:package_id>/", views.book_package, name="book_package"),

    # 🔐 OTP
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),

    # 💳 Payment
    path("payment/<int:booking_id>/", views.payment_pending, name="payment_pending"),
    path("payment-success/<int:booking_id>/", views.payment_success, name="payment_success"),

    # ✅ Success
    path("success/", views.booking_success, name="booking_success"),

    # 🔔 Razorpay Webhook
    path("razorpay/webhook/", views.razorpay_webhook, name="razorpay_webhook"),
]
