from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(
        name="DiagnosticRequest",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120, verbose_name="nombre")),
            ("business", models.CharField(max_length=160, verbose_name="negocio")),
            ("email", models.EmailField(max_length=254, verbose_name="correo electrónico")),
            ("need", models.CharField(choices=[("sales", "Ventas"), ("inventory", "Inventario"), ("security", "Seguridad"), ("integration", "Todo conectado")], max_length=20, verbose_name="necesidad principal")),
            ("message", models.TextField(blank=True, max_length=1000, verbose_name="mensaje")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
        ],
        options={"verbose_name": "solicitud de diagnóstico", "verbose_name_plural": "solicitudes de diagnóstico", "ordering": ["-created_at"]},
    )]
