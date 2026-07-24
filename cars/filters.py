import django_filters
from .models import Car, Brand


class CarFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), label="Brand")
    model_name = django_filters.CharFilter(lookup_expr='icontains', label="Model")
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label="Minimum price")
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label="Maximum price")
    min_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte', label="From the year")
    fuel_type = django_filters.ChoiceFilter(choices=Car.FUEL_CHOICES, label="Fuel type")
    transmission = django_filters.ChoiceFilter(choices=Car.TRANSMISSION_CHOICES, label="transmission")

    class Meta:
        model = Car
        fields = ['brand', 'model_name', 'fuel_type', 'transmission']