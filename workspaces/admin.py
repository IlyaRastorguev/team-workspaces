from django.contrib import admin

from workspaces import models


@admin.register(models.Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("status", "member", "created")
