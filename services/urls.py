from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='services-home'),
    path('service/<int:id>/', views.service_detail, name='service-detail'),
    path('contact/', views.contact, name='contact'),
]
