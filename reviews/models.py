from django.db import models
from django.contrib.auth.models import User
from cars.models import Car


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(verbose_name="نظر شما")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('car', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.car}"