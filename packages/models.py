from django.db import models


class HealthPackage(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    tests_included = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    phone_number = models.CharField(max_length=15)
    package = models.ForeignKey(HealthPackage, on_delete=models.CASCADE)

    # OTP / Verification
    is_verified = models.BooleanField(default=False)

    # PAYMENT PREP
    payment_required = models.BooleanField(default=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        default="pending",
    )
    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.package.name}"
