from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cars.models import Car
from .cart import Cart


@login_required
def cart_add(request, car_id):
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    if car.status != 'available':
        messages.error(request, "Sorry, this vehicle is no longer available.")
    else:
        cart.add(car=car)
        messages.success(request, f"{car} has been added to your cart!")
    return redirect(request.META.get('HTTP_REFERER', 'cars:gallery'))


@login_required
def cart_remove(request, car_id):
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.remove(car)
    messages.warning(request, "Item removed from your cart.")
    return redirect('cart:detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})