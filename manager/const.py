class MessageConst:
    MESSAGE_ID = "messageId"
    MESSAGE_NAME = "messageName"
    PAYLOAD = "payload"


class ErrorConst:
    ERROR_CODE = "error_code"
    ERROR_MESSAGE = "error_message"


class WorkspaceConst:
    ID = "id"
    STATUS = "status"
    MEMBER = "member"
    PROJECT = "project"
    PORT = "port"


class MemberConst:
    ID = "id"
    USER = "user"
    TEAM = "team"


class UserConst:
    USER_NAME = "username"


class TeamConst:
    ID = "id"
    KEY = "key"


class ProjectConst:
    ID = "id"
    NAME = "name"
    STATUS = "status"
    KEY = "key"
    TYPE = "type"
    TEAM = "team"
    REPO = "repo"


class ProjectTypeConst:
    KEY = "key"


class WorkSpaceStatus:
    READY = "READY"
    RUNNING = "RUNNING"
    STOPED = "STOPED"
    ERROR = "ERROR"


class ProjectStatus:
    READY = "READY"
    ERROR = "ERROR"


class MessageName:
    CREATE_PROJECT = "CREATE_PROJECT"
    DELETE_PROJECT = "DELETE_PROJECT"
    CREATE_WORKSPACE = "CREATE_WORKSPACE"
    STOP_WORKSPACE = "STOP_WORKSPACE"
    START_WORKSPACE = "START_WORKSPACE"
    DELETE_WORKSPACE = "DELETE_WORKSPACE"
    ERROR = "ERROR"
