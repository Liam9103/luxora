from decimal import Decimal
from cars.models import Car


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, car):
        car_id = str(car.id)
        if car_id not in self.cart:
            self.cart[car_id] = {'price': str(car.price)}
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, car):
        car_id = str(car.id)
        if car_id in self.cart:
            del self.cart[car_id]
            self.save()

    def __iter__(self):
        """
        Loop over cart items without mutating the raw session dict
        (avoids storing non-JSON-serializable model instances in session).
        """
        car_ids = self.cart.keys()
        cars = Car.objects.filter(id__in=car_ids)
        cars_map = {str(car.id): car for car in cars}

        for car_id, item in self.cart.items():
            car = cars_map.get(car_id)
            if car:
                yield {
                    'car': car,
                    'price': int(item['price']),
                }

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(int(item['price']) for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.save()