# Generated by Django 4.0.3 on 2022-06-10 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64)),
                ("key", models.CharField(default="default", max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("WAIT_FOR_CREATE", "WAIT_FOR_CREATE"),
                            ("WAIT_FOR_DELETE", "WAIT_FOR_DELETE"),
                            ("CREATING", "CREATING"),
                            ("READY", "READY"),
                            ("ERROR", "ERROR"),
                        ],
                        default="WAIT_FOR_CREATE",
                        max_length=32,
                    ),
                ),
                ("key", models.CharField(max_length=512)),
                ("repo", models.CharField(max_length=2048)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="team_projects", to="teams.team"
                    ),
                ),
                ("type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="projects.projecttype")),
            ],
        ),
    ]