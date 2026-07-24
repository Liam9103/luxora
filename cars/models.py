from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Brand name")
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'petrol'),
        ('diesel', 'diesel'),
        ('hybrid', 'hubrid'),
        ('electric', 'electric'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'manual'),
        ('automatic', 'automatic'),
    ]
    STATUS_CHOICES = [
        ('available', 'available'),
        ('sold', 'sold'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars', verbose_name="brand")
    model_name = models.CharField(max_length=100, verbose_name="model")
    year = models.PositiveIntegerField(verbose_name="year built")
    price = models.PositiveBigIntegerField(verbose_name="price")
    mileage = models.PositiveIntegerField(default=0, verbose_name="mileage (Kilometers)")
    color = models.CharField(max_length=50, verbose_name="color")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    description = models.TextField(verbose_name="description")
    main_image = models.ImageField(upload_to='cars/main/', verbose_name="main image")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False, verbose_name="is featured")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.year})"

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='cars/gallery/')

    def __str__(self):
        return f"image {self.car}"