from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Roles:
    DEVELOPER = "DEVELOPER"
    LEAD = "LEAD"
    CHOICES = ((DEVELOPER, DEVELOPER), (LEAD, LEAD))


class Team(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    key = models.CharField(max_length=128, null=False, blank=False, unique=True)


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    team = models.ForeignKey(Team, related_name="team_members", on_delete=models.PROTECT, null=False, blank=False)
    role = models.CharField(max_length=32, choices=Roles.CHOICES, null=False, blank=False, default=Roles.DEVELOPER)
