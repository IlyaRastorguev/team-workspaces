from django.contrib.auth.models import User
from rest_framework import serializers

from teams import models


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "username")


class DefaultTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "name", "key"]


class TeamSerializer(DefaultTeamSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "name", "key", "team_members", "team_projects"]


class DefaultTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeamMember
        fields = ["id", "user", "team", "team_member_workspaces"]


class TeamMemberSerializer(DefaultTeamMemberSerializer):
    user = UsersSerializer()
    team = DefaultTeamSerializer()
