class MessageName:
    CREATE_PROJECT = "CREATE_PROJECT"
    DELETE_PROJECT = "DELETE_PROJECT"
    CREATE_WORKSPACE = "CREATE_WORKSPACE"
    STOP_WORKSPACE = "STOP_WORKSPACE"
    START_WORKSPACE = "START_WORKSPACE"
    DELETE_WORKSPACE = "DELETE_WORKSPACE"
    DONE = "DONE"
    ERROR = "ERROR"


class KafkaConfig:
    CONSUMER = "consumer"
    PRODUCER = "producer"
    CONFIG = "config"
    TOPICS = "topics"
    IN = "in"
    OUT = "out"
    POLL_TIMEOUT = "poll_timeout"
    PROJECTS_KEY = "projects"
    WORKSPACES_KEY = "workspaces"
