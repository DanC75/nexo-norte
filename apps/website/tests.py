from django.test import TestCase
from django.urls import reverse

from apps.diagnostics.models import DiagnosticRequest


class HomeTests(TestCase):
    def test_home_renders_selected_brand_direction(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Impulso Norte")
        self.assertContains(response, "Crece con control")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_valid_diagnostic_request_is_saved(self) -> None:
        response = self.client.post(
            reverse("home"),
            {
                "name": "Laura Gómez",
                "business": "Ferretería El Puente",
                "email": "laura@example.com",
                "need": "inventory",
                "message": "Necesitamos controlar existencias.",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(DiagnosticRequest.objects.count(), 1)

    def test_invalid_diagnostic_request_is_not_saved(self) -> None:
        response = self.client.post(
            reverse("home"),
            {"name": "Laura", "business": "Negocio", "email": "no-es-email", "need": "sales"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiagnosticRequest.objects.count(), 0)
        self.assertContains(response, "Ingrese una dirección de correo electrónico válida")
