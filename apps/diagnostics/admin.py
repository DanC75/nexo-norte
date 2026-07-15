from django.contrib import admin

from .models import DiagnosticRequest


@admin.register(DiagnosticRequest)
class DiagnosticRequestAdmin(admin.ModelAdmin):
    list_display = ("business", "name", "email", "need", "created_at")
    list_filter = ("need", "created_at")
    search_fields = ("business", "name", "email")
    readonly_fields = ("created_at",)
