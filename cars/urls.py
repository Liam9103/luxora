from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('search/', views.ajax_search, name='ajax_search'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('<int:pk>/', views.car_detail, name='detail'),
]
