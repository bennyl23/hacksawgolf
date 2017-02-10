from django.contrib import admin
from team.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ['user', 'tournament', 'golfer']
    list_filter = ['tournament__tournament_name', 'user__user_team_name']


admin.site.register(Team, TeamAdmin)