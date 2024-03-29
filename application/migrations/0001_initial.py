# Generated by Django 5.0 on 2023-12-31 03:43

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NetflixTitle",
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
                ("show_id", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("director", models.CharField(max_length=255)),
                ("cast", models.TextField()),
                ("country", models.CharField(max_length=255)),
                ("date_added", models.CharField(max_length=255)),
                ("release_year", models.IntegerField()),
                ("rating", models.CharField(max_length=255)),
                ("duration", models.CharField(max_length=255)),
                ("listed_in", models.TextField()),
                ("description", models.TextField()),
            ],
        ),
    ]
