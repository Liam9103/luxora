from django.shortcuts import render, redirect
from django.contrib import messages
from cars.models import Car, Brand
from .models import ConsultationRequest


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


def consultation_request(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        preferred_car = request.POST.get('preferred_car', '').strip()
        message = request.POST.get('message', '').strip()

        if not full_name or not email or not phone:
            messages.error(request, 'Please fill in your name, email, and phone number.')
            return redirect('core:home')

        ConsultationRequest.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            preferred_car=preferred_car,
            message=message,
        )
        messages.success(request, 'Your consultation request has been received. We will contact you shortly.')
        return redirect('core:home')

    return redirect('core:home')