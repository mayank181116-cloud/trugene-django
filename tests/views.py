from django.shortcuts import render
from .models import HealthPackage

def package_list(request):
    packages = HealthPackage.objects.filter(is_active=True)
    return render(request, 'packages/package_list.html', {
        'packages': packages
    })
