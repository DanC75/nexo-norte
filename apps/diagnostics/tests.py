from django.test import TestCase

from .models import DiagnosticRequest


class DiagnosticModelTests(TestCase):
    def test_string_representation_identifies_business_and_contact(self) -> None:
        request = DiagnosticRequest(
            name="Laura Gómez",
            business="Ferretería El Puente",
            email="laura@example.com",
            need="inventory",
        )
        self.assertEqual(str(request), "Ferretería El Puente — Laura Gómez")

    def test_country_defaults_to_colombia_and_accepts_peru(self) -> None:
        colombia_request = DiagnosticRequest()
        peru_request = DiagnosticRequest(country=DiagnosticRequest.Country.PERU)
        self.assertEqual(colombia_request.country, DiagnosticRequest.Country.COLOMBIA)
        self.assertEqual(peru_request.get_country_display(), "Perú")
