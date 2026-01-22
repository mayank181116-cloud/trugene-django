from django.contrib import admin
from .models import HealthPackage, Booking


@admin.register(HealthPackage)
class HealthPackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "package",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_verified", "created_at")
    search_fields = ("phone_number",)
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Customer Info", {
            "fields": ("phone_number",)
        }),
        ("Package Details", {
            "fields": ("package",)
        }),
        ("Verification Status", {
            "fields": ("is_verified",)
        }),
        ("System Info", {
            "fields": ("created_at",)
        }),
    )
