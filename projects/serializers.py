from rest_framework import serializers

from projects import models
from teams.serializers import TeamSerializer


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectType
        fields = ["id", "name", "key"]


class DefaultProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id", "name", "status", "key", "type", "team", "repo"]


class ProjectSerializer(DefaultProjectSerializer):
    type = ProjectTypeSerializer()
    team = TeamSerializer()
