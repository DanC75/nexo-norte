import uuid

from django.conf import settings
from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("nombre", max_length=160)
    slug = models.SlugField("identificador", max_length=180, unique=True)
    is_active = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)
    members: models.ManyToManyField = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Membership", related_name="organizations"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "organización"
        verbose_name_plural = "organizaciones"

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Propietario"
        ADMIN = "admin", "Administrador"
        CONSULTANT = "consultant", "Consultor"
        MEMBER = "member", "Colaborador"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField("rol", max_length=20, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"], name="unique_organization_member"
            )
        ]
        verbose_name = "membresía"
        verbose_name_plural = "membresías"

    def __str__(self) -> str:
        return f"{self.user} · {self.organization} · {self.get_role_display()}"
