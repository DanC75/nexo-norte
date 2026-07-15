from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.diagnostics.models import DiagnosticRequest

from .models import AuditEvent


@receiver(post_save, sender=DiagnosticRequest)
def record_diagnostic_creation(
    sender: type[DiagnosticRequest],
    instance: DiagnosticRequest,
    created: bool,
    **kwargs: object,
) -> None:
    if not created:
        return
    transaction.on_commit(
        lambda: AuditEvent.objects.create(
            action="diagnostic.created",
            target_type="diagnostic_request",
            target_id=str(instance.pk),
            metadata={"need": instance.need},
        )
    )
