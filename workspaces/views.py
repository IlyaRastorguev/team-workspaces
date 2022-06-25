import logging

from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view

from workspaces.models import Workspace
from workspaces.serializers import DefaultWorkspaceSerializer, WorkspaceSerializer


@api_view(
    [
        "GET",
    ]
)
def open(request, *args, **kwargs):
    logger = logging.getLogger()
    workspace_id = request.query_params.get("id")
    logger.debug(f"Workspace id: {workspace_id}")
    if workspace_id:
        workspace_obj = Workspace.objects.get(id=workspace_id)
        serializer = WorkspaceSerializer(workspace_obj)
        workspace_data = serializer.data

        project = workspace_data.get("project")

        member = workspace_data.get("member")

        user = member.get("user")

        team = member.get("team")

        workspace_name = f"{team.get('key')}_{user.get('username')}"
        folder = project.get("key")

        response = redirect(f"http://localhost:4444/ws/{workspace_name}/?folder=/{folder}")
        response.headers["Set-Cookie"] = f"workspace={workspace_name}; Path=/; HttpOnly;"

        return response


class WorkspacesView(viewsets.ModelViewSet):
    serializer_class = DefaultWorkspaceSerializer
    queryset = Workspace.objects.all()
