from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("diagnostics", "0002_diagnosticrequest_plan")]

    operations = [
        migrations.AddField(
            model_name="diagnosticrequest",
            name="country",
            field=models.CharField(
                choices=[("co", "Colombia"), ("pe", "Perú")],
                default="co",
                max_length=2,
                verbose_name="país",
            ),
        ),
    ]
