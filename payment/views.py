import random, string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty!")
        return redirect('cars:gallery')

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '')
        # فقط شبیه‌سازی - بدون هیچ اتصال واقعی بانکی
        request.session['pending_total'] = cart.get_total_price()
        request.session['pending_car_ids'] = list(request.session.get('cart', {}).keys())
        return redirect('payment:gateway')

    return render(request, 'payment/checkout.html', {'cart': cart})


@login_required
def gateway(request):
    total = request.session.get('pending_total')
    if not total:
        return redirect('cars:gallery')

    if request.method == 'POST':
        # شبیه‌سازی پرداخت - هر شماره کارت 16 رقمی تایید میشه
        tracking_code = ''.join(random.choices(string.digits, k=12))
        car_ids = request.session.get('pending_car_ids', [])

        from cars.models import Car
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='paid',
            tracking_code=tracking_code,
        )
        cars = Car.objects.filter(id__in=car_ids)
        order.cars.set(cars)
        cars.update(status='sold')

        cart = Cart(request)
        cart.clear()
        request.session.pop('pending_total', None)
        request.session.pop('pending_car_ids', None)

        messages.success(request, "Payment completed successfully!")
        return redirect('payment:success', order_id=order.id)

    return render(request, 'payment/gateway.html', {'total': total})


@login_required
def payment_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'payment/success.html', {'order': order})