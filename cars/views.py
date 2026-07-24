from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Car
from .filters import CarFilter
from reviews.models import Review
from reviews.forms import ReviewForm


def gallery(request):
    cars_qs = Car.objects.filter(status='available')
    car_filter = CarFilter(request.GET, queryset=cars_qs)
    paginator = Paginator(car_filter.qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cars/gallery.html', {
        'filter': car_filter,
        'page_obj': page_obj,
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    reviews = car.reviews.select_related('user').order_by('-created_at')
    form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            from django.shortcuts import redirect
            return redirect('cars:detail', pk=pk)

    related_cars = Car.objects.filter(brand=car.brand, status='available').exclude(pk=pk)[:4]

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'reviews': reviews,
        'form': form,
        'related_cars': related_cars,
    })