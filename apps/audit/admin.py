from django.contrib import admin
from django.http import HttpRequest

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("action", "target_type", "target_id", "actor", "organization", "created_at")
    list_filter = ("action", "target_type", "created_at")
    search_fields = ("target_id", "request_id")
    readonly_fields = (
        "id",
        "organization",
        "actor",
        "action",
        "target_type",
        "target_id",
        "metadata",
        "request_id",
        "created_at",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: AuditEvent | None = None) -> bool:
        return False
