import random

from agents import Agent
from const import (
    ErrorConst,
    MemberConst,
    MessageConst,
    MessageName,
    ProjectConst,
    ProjectStatus,
    ProjectTypeConst,
    TeamConst,
    UserConst,
    WorkspaceConst,
    WorkSpaceStatus,
)

IDE_CONTAINER_PORT = 8000


class Handler:
    def __init__(self, agent: Agent):
        self._agent = agent

    def _handle_error(self, message: str, code: int, stdout: str):
        message[MessageConst.MESSAGE_NAME] = MessageName.ERROR
        message[MessageConst.PAYLOAD][ErrorConst.ERROR_CODE] = code
        message[MessageConst.PAYLOAD][ErrorConst.ERROR_MESSAGE] = stdout

    def get_consumer_topic(self, config):
        return config["topics"][self._config_key]["in"]

    def get_producer_topic(self, config):
        return config["topics"][self._config_key]["out"]

    def create(self, message: dict) -> None:
        pass

    def delete(self, message: dict) -> None:
        pass

    def start(self, message: dict) -> None:
        pass

    def stop(self, message: dict) -> None:
        pass

    def handle(self, message: dict) -> dict:
        pass


class ProjectHandler(Handler):
    _config_key = "projects"

    def _get_project_image_name(self, project: dict) -> str:
        return project.get(ProjectConst.KEY)

    def _get_project_image_type(self, project: dict) -> str:
        return project.get(ProjectConst.TYPE, {}).get(ProjectTypeConst.KEY)

    def _get_project_repo(self, project: dict) -> str:
        return project.get(ProjectConst.REPO)

    def create(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)

        image_name = self._get_project_image_name(payload)
        image_type = self._get_project_image_type(payload)

        project_repo = self._get_project_repo(payload)

        process = self._agent.build_image(image_name, image_type, project_repo)

        if process.returncode == 0:
            payload = {}

            payload[ProjectConst.ID] = message[MessageConst.PAYLOAD][ProjectConst.ID]
            payload[ProjectConst.STATUS] = ProjectStatus.READY

            message[MessageConst.PAYLOAD] = payload
        else:
            self._handle_error(message, process.returncode, process.stdout)

    def delete(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)

        image_name = self._get_project_image_name(payload)

        process = self._agent.remove_image(image_name)

        if process.returncode != 0:
            self._handle_error(message, process.returncode, process.stdout)

    def handle(self, message: dict) -> dict:
        message_name = message.get(MessageConst.MESSAGE_NAME)

        if message_name == MessageName.CREATE_PROJECT:
            self.create(message)

        elif message_name == MessageName.DELETE_PROJECT:
            self.delete(message)

        return message


class WorkspaceHandler(ProjectHandler):
    _config_key = "workspaces"

    def _get_workspace_container_name(self, workspace: dict) -> str:
        member = workspace.get(WorkspaceConst.MEMBER)
        user = member.get(MemberConst.USER)
        team = member.get(MemberConst.TEAM)

        return f"{team.get(TeamConst.KEY)}_{user.get(UserConst.USER_NAME)}"

    def _get_workspace_container_port(self) -> str:

        return random.randint(1024, 49151)

    def _get_workspace_image_name(self, workspace: dict) -> str:
        project = workspace.get(WorkspaceConst.PROJECT)

        return self._get_project_image_name(project)

    def create(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)

        project_image_name = self._get_workspace_image_name(payload)
        container_name = self._get_workspace_container_name(payload)
        container_port = self._get_workspace_container_port()

        process = self._agent.create_container(project_image_name, container_name, container_port, IDE_CONTAINER_PORT)

        if process.returncode == 0:
            payload = {}

            payload[WorkspaceConst.ID] = message[MessageConst.PAYLOAD][WorkspaceConst.ID]
            payload[WorkspaceConst.STATUS] = WorkSpaceStatus.READY
            payload[WorkspaceConst.PORT] = container_port

            message[MessageConst.PAYLOAD] = payload
        else:
            self._handle_error(message, process.returncode, process.stdout)

    def start(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)
        container_name = self._get_workspace_container_name(payload)

        process = self._agent.start_container(container_name)

        if process.returncode == 0:
            payload = {}

            payload[WorkspaceConst.ID] = message[MessageConst.PAYLOAD][WorkspaceConst.ID]
            payload[WorkspaceConst.STATUS] = WorkSpaceStatus.RUNNING

            message[MessageConst.PAYLOAD] = payload
        else:
            self._handle_error(message, process.returncode, process.stdout)

    def stop(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)
        container_name = self._get_workspace_container_name(payload)

        process = self._agent.stop_container(container_name)

        if process.returncode == 0:
            payload = {}

            payload[WorkspaceConst.ID] = message[MessageConst.PAYLOAD][WorkspaceConst.ID]
            payload[WorkspaceConst.STATUS] = WorkSpaceStatus.STOPED

            message[MessageConst.PAYLOAD] = payload
        else:
            self._handle_error(message, process.returncode, process.stdout)

    def delete(self, message: dict):
        payload = message.get(MessageConst.PAYLOAD)
        container_name = self._get_workspace_container_name(payload)

        process = self._agent.remove_container(container_name)

        if process.returncode != 0:
            self._handle_error(message, process.returncode, process.stdout)

    def handle(self, message: dict) -> dict:
        message_name = message.get(MessageConst.MESSAGE_NAME)

        if message_name == MessageName.CREATE_WORKSPACE:
            self.create(message)

        elif message_name == MessageName.START_WORKSPACE:
            self.start(message)

        elif message_name == MessageName.STOP_WORKSPACE:
            self.stop(message)

        elif message_name == MessageName.DELETE_WORKSPACE:
            self.delete(message)

        return message
