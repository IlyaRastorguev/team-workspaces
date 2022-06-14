from django.db import models

from projects.models import Project
from teams.models import TeamMember


class Status:
    WAIT_FOR_CREATE = "WAIT_FOR_CREATE"
    WAIT_FOR_START = "WAIT_FOR_START"
    WAIT_FOR_STOP = "WAIT_FOR_STOP"
    WAIT_FOR_DELETE = "WAIT_FOR_DELETE"
    READY = "READY"
    RUNNING = "RUNNING"
    STOPED = "STOPED"
    ERROR = "ERROR"
    CHOICES = (
        (WAIT_FOR_CREATE, WAIT_FOR_CREATE),
        (WAIT_FOR_START, WAIT_FOR_START),
        (WAIT_FOR_STOP, WAIT_FOR_STOP),
        (WAIT_FOR_DELETE, WAIT_FOR_DELETE),
        (READY, READY),
        (RUNNING, RUNNING),
        (STOPED, STOPED),
        (ERROR, ERROR),
    )


class Workspace(models.Model):
    status = models.CharField(
        max_length=32, choices=Status.CHOICES, null=False, blank=False, default=Status.WAIT_FOR_CREATE
    )
    member = models.ForeignKey(
        TeamMember, related_name="team_member_workspaces", on_delete=models.PROTECT, null=False, blank=False
    )
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    port = models.IntegerField()

    class Meta:
        ordering = ["-created"]
