from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Car, WishlistItem
from .filters import CarFilter
from reviews.forms import ReviewForm


def gallery(request):
    # reduce DB queries by joining brand and prefetching images
    cars_qs = Car.objects.filter(status='available').select_related('brand').prefetch_related('gallery_images')
    car_filter = CarFilter(request.GET, queryset=cars_qs)
    queryset = car_filter.qs
    # Global quick search from navbar (searches brand name and model)
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(models.Q(brand__name__icontains=q) | models.Q(model_name__icontains=q))

    sort_by = request.GET.get('sort_by', '-created_at')
    allowed_sort = {'-created_at': '-created_at', 'price': 'price', '-price': '-price', 'year': 'year', '-year': '-year'}
    if sort_by in allowed_sort:
        queryset = queryset.order_by(allowed_sort[sort_by])
    else:
        queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cars/gallery.html', {
        'filter': car_filter,
        'page_obj': page_obj,
        'sort_by': sort_by,
    })


def ajax_search(request):
    q = request.GET.get('q', '').strip()
    qs = Car.objects.filter(status='available')
    if q:
        qs = qs.filter(models.Q(brand__name__icontains=q) | models.Q(model_name__icontains=q))
    qs = qs.select_related('brand')[:12]
    # render a small partial
    from django.template.loader import render_to_string
    html = render_to_string('cars/_gallery_results_partial.html', {'cars': qs, 'selected_car_ids': []}, request=request)
    from django.http import JsonResponse
    return JsonResponse({'html': html})


@login_required
def toggle_wishlist(request, pk):
    car = get_object_or_404(Car, pk=pk)
    item, created = WishlistItem.objects.get_or_create(user=request.user, car=car)
    if not created:
        item.delete()
        messages.success(request, 'Removed from wishlist.')
    else:
        messages.success(request, 'Added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER') or 'cars:gallery')


@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('car', 'car__brand')
    return render(request, 'cars/wishlist.html', {'items': items})


def car_detail(request, pk):
    # fetch related objects to avoid N+1 queries for brand, gallery images and reviews
    qs = Car.objects.select_related('brand').prefetch_related('gallery_images', 'reviews__user')
    car = get_object_or_404(qs, pk=pk)
    reviews = car.reviews.all().select_related('user').order_by('-created_at')
    form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('cars:detail', pk=pk)

    related_cars = Car.objects.filter(brand=car.brand, status='available').exclude(pk=pk)[:4]
    in_wishlist = request.user.is_authenticated and WishlistItem.objects.filter(user=request.user, car=car).exists()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'reviews': reviews,
        'form': form,
        'related_cars': related_cars,
        'in_wishlist': in_wishlist,
    })