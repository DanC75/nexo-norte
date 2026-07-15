import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Organization", fields=[
            ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ("name", models.CharField(max_length=160, verbose_name="nombre")),
            ("slug", models.SlugField(max_length=180, unique=True, verbose_name="identificador")),
            ("is_active", models.BooleanField(default=True, verbose_name="activa")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
        ], options={"verbose_name": "organización", "verbose_name_plural": "organizaciones", "ordering": ["name"]}),
        migrations.CreateModel(name="Membership", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("role", models.CharField(choices=[("owner", "Propietario"), ("admin", "Administrador"), ("consultant", "Consultor"), ("member", "Colaborador")], default="member", max_length=20, verbose_name="rol")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
            ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="organizations.organization")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to=settings.AUTH_USER_MODEL)),
        ], options={"verbose_name": "membresía", "verbose_name_plural": "membresías"}),
        migrations.AddField(model_name="organization", name="members", field=models.ManyToManyField(related_name="organizations", through="organizations.Membership", to=settings.AUTH_USER_MODEL)),
        migrations.AddConstraint(model_name="membership", constraint=models.UniqueConstraint(fields=("organization", "user"), name="unique_organization_member")),
    ]
