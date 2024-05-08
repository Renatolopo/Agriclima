# Generated by Django 4.2.6 on 2024-05-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Estacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Codigo", models.CharField(max_length=100)),
                ("Nome", models.CharField(max_length=500)),
                ("Latitude", models.CharField(max_length=100)),
                ("Longitude", models.CharField(max_length=100)),
                ("TipoEstacao", models.CharField(max_length=100)),
            ],
        ),
    ]
