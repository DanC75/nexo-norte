from django.test import TestCase
from django.urls import reverse

from apps.diagnostics.models import DiagnosticRequest


class HomeTests(TestCase):
    def test_home_renders_selected_brand_direction(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Impulso Norte")
        self.assertContains(response, "Crece con control")
        self.assertContains(response, "Explorar soluciones")
        self.assertContains(response, "Planes y precios")
        self.assertContains(response, "Solicitar diagnóstico")
        self.assertNotContains(response, '<form method="post"')
        self.assertNotContains(response, 'class="decision-path')
        self.assertNotContains(response, 'class="home-plans')
        self.assertNotContains(response, 'class="service-preview')
        self.assertNotContains(response, 'class="sector-grid')
        self.assertNotContains(response, 'class="method-steps')
        self.assertNotContains(response, "Norte Base")
        self.assertNotContains(response, "Ventas digitales")
        self.assertNotContains(response, "Explorar las 6 soluciones")
        self.assertContains(response, "Explorar soluciones", count=1)
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

    def test_home_does_not_accept_diagnostic_submissions(self) -> None:
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
        self.assertEqual(response.status_code, 405)
        self.assertEqual(DiagnosticRequest.objects.count(), 0)


class PublicPageTests(TestCase):
    def test_all_company_pages_render(self) -> None:
        page_names = ("solutions", "method", "cases", "about", "plans", "contact", "privacy")
        for name in page_names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_regional_coverage_exposes_colombia_and_peru(self) -> None:
        plans_response = self.client.get(reverse("plans"))
        self.assertContains(plans_response, "Colombia · COP")
        self.assertContains(plans_response, "Perú · PEN")
        self.assertContains(plans_response, "S/ 1,450")
        self.assertContains(plans_response, "S/ 3,800")
        self.assertContains(plans_response, "data-region-dialog", count=1)
        self.assertContains(plans_response, "¿Estás en")

        privacy_response = self.client.get(reverse("privacy"))
        self.assertContains(privacy_response, "sin solicitar ubicación GPS")

        solutions_response = self.client.get(reverse("solutions"))
        self.assertContains(solutions_response, 'data-pe-value="25"')
        self.assertContains(solutions_response, 'data-pe="PEN"')

    def test_global_navigation_is_not_duplicated(self) -> None:
        response = self.client.get(reverse("home"))
        html = response.content
        self.assertEqual(html.count(b'id="site-nav"'), 1)
        self.assertEqual(html.count(b'class="mobile-action-dock"'), 1)
        self.assertEqual(html.count(b'<main id="contenido">'), 1)

    def test_diagnostic_form_has_one_canonical_page(self) -> None:
        pages_without_form = (
            "home",
            "solutions",
            "method",
            "cases",
            "about",
            "plans",
            "privacy",
        )
        for name in pages_without_form:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertNotContains(response, '<form method="post"')
                self.assertNotContains(response, 'class="closing-cta')

        contact_response = self.client.get(reverse("contact"))
        self.assertContains(contact_response, '<form method="post"', count=1)
        self.assertNotContains(contact_response, 'class="nav-cta"')
        self.assertContains(contact_response, ">Inicio</a>")

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
                "country": "pe",
                "email": "carlos@example.com",
                "need": "security",
                "plan": "norte-conecta",
                "message": "Necesitamos revisar accesos y respaldos.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(DiagnosticRequest.objects.count(), 1)
        self.assertEqual(DiagnosticRequest.objects.get().plan, "norte-conecta")
        self.assertEqual(DiagnosticRequest.objects.get().country, "pe")

    def test_invalid_contact_request_is_not_saved(self) -> None:
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Laura",
                "business": "Negocio",
                "country": "co",
                "email": "no-es-email",
                "need": "sales",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiagnosticRequest.objects.count(), 0)
        self.assertContains(response, "Ingrese una dirección de correo electrónico válida")

    def test_contact_honeypot_rejects_automated_submission(self) -> None:
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Robot",
                "business": "Spam",
                "country": "co",
                "email": "robot@example.com",
                "need": "sales",
                "website": "https://spam.example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiagnosticRequest.objects.count(), 0)
        self.assertContains(response, "No fue posible procesar la solicitud")

    def test_plan_link_preselects_contact_form(self) -> None:
        response = self.client.get(reverse("contact"), {"plan": "norte-base"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="norte-base" selected>')

    def test_unknown_plan_is_not_preselected(self) -> None:
        response = self.client.get(reverse("contact"), {"plan": "inventado"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<option value="inventado" selected>')
