from django.contrib import admin

from teams import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.TeamMember)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ("user", "team")
