from django.db import models


class DiagnosticRequest(models.Model):
    class Need(models.TextChoices):
        SALES = "sales", "Ventas"
        INVENTORY = "inventory", "Inventario"
        SECURITY = "security", "Seguridad"
        INTEGRATION = "integration", "Todo conectado"

    class Plan(models.TextChoices):
        BASE = "norte-base", "Norte Base"
        CONNECT = "norte-conecta", "Norte Conecta"
        SCALE = "norte-escala", "Norte Escala"

    name = models.CharField("nombre", max_length=120)
    business = models.CharField("negocio", max_length=160)
    email = models.EmailField("correo electrónico")
    need = models.CharField("necesidad principal", max_length=20, choices=Need.choices)
    plan = models.CharField("plan de interés", max_length=20, choices=Plan.choices, blank=True)
    message = models.TextField("mensaje", max_length=1000, blank=True)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "solicitud de diagnóstico"
        verbose_name_plural = "solicitudes de diagnóstico"

    def __str__(self) -> str:
        return f"{self.business} — {self.name}"
