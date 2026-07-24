from django.db import models
from django.contrib.auth.models import User
from cars.models import Car


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('failed', 'failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car)
    total_price = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"