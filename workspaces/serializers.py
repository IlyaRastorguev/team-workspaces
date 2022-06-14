from rest_framework import serializers

from projects.serializers import ProjectSerializer
from teams.serializers import TeamMemberSerializer
from workspaces import models


class DefaultWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workspace
        fields = ["id", "status", "member", "project", "port", "created"]


class WorkspaceSerializer(DefaultWorkspaceSerializer):
    project = ProjectSerializer()
    member = TeamMemberSerializer()
