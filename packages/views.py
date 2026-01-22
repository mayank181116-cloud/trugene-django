from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import random

from .models import HealthPackage, Booking
from tests.models import MobileOTP


# =========================
# DEV OTP SENDER
# =========================
def send_otp_sms(phone, otp):
    print("🔐 DEV OTP for", phone, ":", otp)


# =========================
# PACKAGE LIST
# =========================
def package_list(request):
    packages = HealthPackage.objects.filter(is_active=True)
    return render(request, 'packages/package_list.html', {
        'packages': packages
    })


# =========================
# BOOK PACKAGE
# =========================
def book_package(request, package_id):
    package = get_object_or_404(HealthPackage, id=package_id)

    if request.method == "POST":
        phone = request.POST.get('phone', '').strip()

        booking = Booking.objects.create(
            phone_number=phone,
            package=package
        )

        # Remove old OTPs
        MobileOTP.objects.filter(mobile=phone).delete()

        otp = ''.join(random.choices('0123456789', k=6))

        MobileOTP.objects.create(
            mobile=phone,
            otp=otp
        )

        send_otp_sms(phone, otp)

        request.session['phone'] = phone
        request.session['booking_id'] = booking.id

        return redirect('packages:verify_otp')

    return render(request, 'packages/book_package.html', {
        'package': package
    })


# =========================
# VERIFY OTP (HARD BIND)
# =========================
def verify_otp(request):
    phone = request.session.get('phone')
    booking_id = request.session.get('booking_id')

    if not phone or not booking_id:
        return redirect('packages:package_list')

    otp_obj = MobileOTP.objects.filter(
        mobile=phone
    ).order_by('-created_at').first()

    if not otp_obj or otp_obj.is_expired():
        MobileOTP.objects.filter(mobile=phone).delete()
        return render(request, 'packages/verify_otp.html', {
            'error': 'OTP expired. Please resend.'
        })

    # ❌ Max attempts reached
    if otp_obj.attempt_count >= settings.OTP_MAX_ATTEMPTS:
        MobileOTP.objects.filter(mobile=phone).delete()
        return render(request, 'packages/verify_otp.html', {
            'error': 'Too many wrong attempts. OTP blocked.'
        })

    if request.method == "POST":
        entered_otp = request.POST.get('otp', '').strip()

        if otp_obj.otp != entered_otp:
            otp_obj.attempt_count += 1
            otp_obj.save()
            return render(request, 'packages/verify_otp.html', {
                'error': 'Invalid OTP'
            })

        # ✅ OTP SUCCESS
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            is_verified=False
        )
        booking.is_verified = True
        booking.save()

        MobileOTP.objects.filter(mobile=phone).delete()

        # IMPORTANT: Do NOT flush full session yet
        return redirect('packages:payment_pending', booking_id=booking.id)

    return render(request, 'packages/verify_otp.html')


# =========================
# RESEND OTP
# =========================
def resend_otp(request):
    phone = request.session.get('phone')

    if not phone:
        return redirect('packages:package_list')

    last_otp = MobileOTP.objects.filter(
        mobile=phone
    ).order_by('-created_at').first()

    if last_otp and last_otp.resend_count >= settings.OTP_RESEND_LIMIT:
        return render(request, 'packages/verify_otp.html', {
            'error': 'OTP resend limit reached'
        })

    MobileOTP.objects.filter(mobile=phone).delete()

    otp = ''.join(random.choices('0123456789', k=6))
    resend_count = last_otp.resend_count + 1 if last_otp else 1

    MobileOTP.objects.create(
        mobile=phone,
        otp=otp,
        resend_count=resend_count
    )

    send_otp_sms(phone, otp)

    return redirect('packages:verify_otp')


# =========================
# PAYMENT PENDING
# =========================
def payment_pending(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.payment_status == "paid":
        return redirect("packages:booking_success")

    return render(request, "packages/payment_pending.html", {
        "booking": booking
    })


# =========================
# PAYMENT SUCCESS
# =========================
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.payment_status = "paid"
    booking.payment_reference = "DUMMY_REF_123"
    booking.save()

    # Clear session AFTER payment
    request.session.flush()

    return redirect("packages:booking_success")


# =========================
# SUCCESS
# =========================
def booking_success(request):
    return render(request, 'packages/booking_success.html')

