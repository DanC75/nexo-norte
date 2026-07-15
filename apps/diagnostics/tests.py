from django.test import TestCase
from .models import DiagnosticRequest


class DiagnosticModelTests(TestCase):
    def test_string_representation_identifies_business_and_contact(self):
        request = DiagnosticRequest(name="Laura Gómez", business="Ferretería El Puente", email="laura@example.com", need="inventory")
        self.assertEqual(str(request), "Ferretería El Puente — Laura Gómez")
