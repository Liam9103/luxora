from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Brand, Car, WishlistItem


class WishlistItemModelTests(TestCase):
    def test_user_can_save_a_car_to_wishlist_once(self):
        user = get_user_model().objects.create_user(username='tester', password='123456')
        brand = Brand.objects.create(name='BMW')
        image = SimpleUploadedFile('car.png', b'fake-image-bytes', content_type='image/png')
        car = Car.objects.create(
            brand=brand,
            model_name='M3',
            year=2023,
            price=120000,
            mileage=1000,
            color='Black',
            description='Great car',
            main_image=image,
        )

        item = WishlistItem.objects.create(user=user, car=car)

        self.assertEqual(item.user, user)
        self.assertEqual(item.car, car)
        self.assertEqual(WishlistItem.objects.filter(user=user, car=car).count(), 1)
