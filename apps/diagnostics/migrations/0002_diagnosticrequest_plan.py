from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("diagnostics", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="diagnosticrequest",
            name="plan",
            field=models.CharField(
                blank=True,
                choices=[
                    ("norte-base", "Norte Base"),
                    ("norte-conecta", "Norte Conecta"),
                    ("norte-escala", "Norte Escala"),
                ],
                max_length=20,
                verbose_name="plan de interés",
            ),
        ),
    ]
