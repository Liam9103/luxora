from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<int:pk>/', views.car_detail, name='detail'),
]