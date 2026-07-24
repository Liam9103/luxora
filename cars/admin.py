from django.contrib import admin
from .models import Brand, Car, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_name', 'year', 'price', 'status', 'is_featured']
    list_filter = ['brand', 'status', 'fuel_type', 'transmission', 'is_featured']
    search_fields = ['model_name', 'brand__name']
    inlines = [CarImageInline]