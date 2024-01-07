# Generated by Django 5.0 on 2023-12-31 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=255)),
                ("iso2", models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name="Title",
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
                ("show_title", models.CharField(max_length=255)),
                ("season_title", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="WeeklyRanking",
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
                ("week", models.DateField()),
                ("category", models.CharField(max_length=255)),
                ("weekly_rank", models.IntegerField()),
                ("cumulative_weeks_in_top_10", models.IntegerField()),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.country",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.title",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="NetflixTitle",
        ),
    ]