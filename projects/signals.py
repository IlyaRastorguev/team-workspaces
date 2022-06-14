import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project, Status
from projects.project_manager import ProjectManager

manager = ProjectManager(settings.KAFKA_CONFIG)


@receiver(post_save, sender=Project)
def ProjectsSignal(instance: Project, created, **kwargs):
    if not manager.is_subscribed():
        manager.subscribe()

    logger = logging.getLogger()
    logger.debug(f"Workspace signal received. workspace: {instance.id}")
    status = instance.status

    if status == Status.WAIT_FOR_CREATE:
        manager.create(instance)
    elif status == Status.WAIT_FOR_DELETE:
        manager.delete(instance)
