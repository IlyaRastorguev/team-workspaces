from django.db import models

from teams.models import Team


class Status:
    WAIT_FOR_CREATE = "WAIT_FOR_CREATE"
    WAIT_FOR_DELETE = "WAIT_FOR_DELETE"
    CREATING = "CREATING"
    READY = "READY"
    ERROR = "ERROR"
    CHOICES = (
        (WAIT_FOR_CREATE, WAIT_FOR_CREATE),
        (WAIT_FOR_DELETE, WAIT_FOR_DELETE),
        (CREATING, CREATING),
        (READY, READY),
        (ERROR, ERROR),
    )


class ProjectType(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    key = models.CharField(max_length=64, null=False, blank=False, default="default")


class Project(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    status = models.CharField(
        max_length=32, choices=Status.CHOICES, null=False, blank=False, default=Status.WAIT_FOR_CREATE
    )
    key = models.CharField(max_length=512, null=False, blank=False)
    type = models.ForeignKey(ProjectType, on_delete=models.PROTECT, null=False, blank=False)
    team = models.ForeignKey(Team, related_name="team_projects", on_delete=models.PROTECT, null=False, blank=False)
    repo = models.CharField(max_length=2048, null=False, blank=False)
