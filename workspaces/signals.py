import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from workspaces.models import Status, Workspace
from workspaces.workspace_manager import WorkspaceManager

manager = WorkspaceManager(settings.KAFKA_CONFIG)


@receiver(post_save, sender=Workspace)
def WorkspaceSignal(instance: Workspace, created, update_fields, **kwargs):
    if not manager.is_subscribed():
        manager.subscribe()

    logger = logging.getLogger()
    logger.debug(f"Workspace signal received. workspace: {instance.id}")
    status = instance.status

    if status == Status.WAIT_FOR_CREATE:
        manager.create(instance)
    elif status == Status.WAIT_FOR_START:
        manager.start(instance)
    elif status == Status.WAIT_FOR_STOP:
        manager.stop(instance)
    elif status == Status.WAIT_FOR_DELETE:
        manager.delete(instance)
