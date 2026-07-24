from django.shortcuts import render
from cars.models import Car, Brand


def home(request):
    featured_cars = Car.objects.filter(is_featured=True, status='available')[:6]
    latest_cars = Car.objects.filter(status='available').order_by('-created_at')[:8]
    brands = Brand.objects.all()
    return render(request, 'core/home.html', {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'brands': brands,
    })


def about(request):
    return render(request, 'core/about.html')