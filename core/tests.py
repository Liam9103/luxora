from django.test import TestCase

from .models import ConsultationRequest


class ConsultationRequestModelTests(TestCase):
    def test_consultation_request_str_representation(self):
        request = ConsultationRequest.objects.create(
            full_name='Ali Reza',
            email='ali@example.com',
            phone='09120000000',
            preferred_car='BMW M3',
            message='Please contact me',
        )

        self.assertEqual(str(request), 'Ali Reza - BMW M3')
