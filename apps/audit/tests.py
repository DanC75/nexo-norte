from django.test import TestCase

from apps.diagnostics.models import DiagnosticRequest

from .models import AuditEvent


class AuditSignalTests(TestCase):
    def test_diagnostic_creation_is_audited(self) -> None:
        with self.captureOnCommitCallbacks(execute=True):
            diagnostic = DiagnosticRequest.objects.create(
                name="Laura", business="Comercio", email="laura@example.com", need="security"
            )
        event = AuditEvent.objects.get(action="diagnostic.created")

        self.assertEqual(event.target_id, str(diagnostic.pk))
        self.assertEqual(event.metadata, {"need": "security"})
