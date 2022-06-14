# Generated by Django 4.0.3 on 2022-06-10 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "0001_initial"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Workspace",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("WAIT_FOR_CREATE", "WAIT_FOR_CREATE"),
                            ("WAIT_FOR_START", "WAIT_FOR_START"),
                            ("WAIT_FOR_STOP", "WAIT_FOR_STOP"),
                            ("WAIT_FOR_DELETE", "WAIT_FOR_DELETE"),
                            ("READY", "READY"),
                            ("RUNNING", "RUNNING"),
                            ("STOPED", "STOPED"),
                            ("ERROR", "ERROR"),
                        ],
                        default="WAIT_FOR_CREATE",
                        max_length=32,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("port", models.IntegerField()),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="team_member_workspaces",
                        to="teams.teammember",
                    ),
                ),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="projects.project")),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
    ]
