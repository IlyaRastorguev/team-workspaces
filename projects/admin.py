from django.contrib import admin

from projects import models


@admin.register(models.ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "key")


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "repo")
