from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Contact


def home(request):
    services = Service.objects.all()
    return render(request, 'services/home.html', {'services': services})


def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/service_detail.html', {'service': service})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(request, "Thank you! We will contact you soon.")
        return redirect('contact')

    return render(request, 'services/contact.html')
