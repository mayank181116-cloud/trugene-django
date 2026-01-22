from django.urls import path, include

urlpatterns = [
    path("packages/", include("packages.urls")),
]
