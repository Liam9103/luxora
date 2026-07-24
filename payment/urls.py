from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('gateway/', views.gateway, name='gateway'),
    path('success/<int:order_id>/', views.payment_success, name='success'),
]