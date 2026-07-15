from django.test import TestCase
from django.urls import reverse

from apps.diagnostics.models import DiagnosticRequest


class HomeTests(TestCase):
    def test_home_renders_selected_brand_direction(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Impulso Norte")
        self.assertContains(response, "Crece con control")
        self.assertContains(response, "¿Qué necesitas resolver hoy?")
        self.assertContains(response, "Planes y precios")
        self.assertContains(response, "Solicitar diagnóstico")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

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

    def test_honeypot_rejects_automated_submission(self) -> None:
        response = self.client.post(
            reverse("home"),
            {
                "name": "Robot",
                "business": "Spam",
                "email": "robot@example.com",
                "need": "sales",
                "website": "https://spam.example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiagnosticRequest.objects.count(), 0)
        self.assertContains(response, "No fue posible procesar la solicitud")


class PublicPageTests(TestCase):
    def test_all_company_pages_render(self) -> None:
        page_names = ("solutions", "method", "cases", "about", "plans", "contact", "privacy")
        for name in page_names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_global_navigation_is_not_duplicated(self) -> None:
        response = self.client.get(reverse("home"))
        html = response.content
        self.assertEqual(html.count(b'id="site-nav"'), 1)
        self.assertEqual(html.count(b'class="mobile-action-dock"'), 1)
        self.assertEqual(html.count(b'<main id="contenido">'), 1)

    def test_solution_detail_renders_known_service(self) -> None:
        response = self.client.get(reverse("solution_detail", args=["seguridad-practica"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seguridad práctica")
        self.assertContains(response, "Matriz de accesos")

    def test_unknown_solution_returns_not_found(self) -> None:
        response = self.client.get(reverse("solution_detail", args=["no-existe"]))
        self.assertEqual(response.status_code, 404)

    def test_contact_page_saves_diagnostic_request(self) -> None:
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Carlos Ruiz",
                "business": "Distribuciones Norte",
                "email": "carlos@example.com",
                "need": "security",
                "plan": "norte-conecta",
                "message": "Necesitamos revisar accesos y respaldos.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(DiagnosticRequest.objects.count(), 1)
        self.assertEqual(DiagnosticRequest.objects.get().plan, "norte-conecta")

    def test_plan_link_preselects_contact_form(self) -> None:
        response = self.client.get(reverse("contact"), {"plan": "norte-base"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="norte-base" selected>')

    def test_unknown_plan_is_not_preselected(self) -> None:
        response = self.client.get(reverse("contact"), {"plan": "inventado"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<option value="inventado" selected>')
