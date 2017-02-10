from team.models import Team


def delete_team(user_id, tournament_id):
    Team.objects.filter(user__user_id=user_id, tournament__tournament_id=tournament_id).delete()
