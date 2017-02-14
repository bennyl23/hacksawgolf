from django.contrib import admin
from tournament.models import Tournament, TournamentParticipant, TournamentType
from django.db import models
from django.forms import TextInput


class TournamentAdmin(admin.ModelAdmin):
    fields = ['tournament_name', 'tournament_location', 'tournament_abbrv', 'tournament_week', 'start_date', 'end_date', 'picks_lock_date', 'tournament_type', 'anyone', 'multiwin', 'in_contention', 'cut_point', 'ready_for_picks', 'tournament_winner', 'tournament_winnings', 'tournament_second_place', 'tournament_second_place_winnings']
    list_display = ['tournament_name', 'start_date', 'end_date', 'picks_lock_date', 'ready_for_picks']
    list_editable = ['ready_for_picks']
    list_per_page = 1000
    ordering = ('tournament_week',)


class TournamentTypeAdmin(admin.ModelAdmin):
    fields = ['tournament_type', 'tournament_type_five_mdc', 'tournament_type_six_mdc', 'tournament_type_winnings_multiplier']
    list_display = ['tournament_type', 'tournament_type_five_mdc', 'tournament_type_six_mdc', 'tournament_type_winnings_multiplier']


class TournamentParticipantAdmin(admin.ModelAdmin):
    # default tournament to the current tournament
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tournament':
            kwargs['initial'] = Tournament.objects.current_tournament()
        return super(TournamentParticipantAdmin, self).formfield_for_foreignkey (db_field, request, **kwargs)

    fields = ['tournament', 'golfer', 'salary', 'score_to_par', 'winnings', 'status', 'made_the_cut']
    list_display = ['get_golfer_lname', 'get_golfer_fname', 'tournament', 'salary', 'score_to_par', 'winnings', 'status', 'made_the_cut']
    list_editable = ['salary', 'score_to_par', 'winnings', 'status', 'made_the_cut']
    list_per_page = 300
    list_filter = ['made_the_cut', 'tournament']
    ordering = ('-tournament__tournament_week', 'golfer__golfer_lname',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'10'})}
    }
    class Media:
        js = {
              #'/static/tournament/admin/tournament_participant_admin.js'
              'tournament/static/tournament/admin/tournament_participant_admin.js'
        }

    def get_golfer_lname(self, obj):
        return obj.golfer.golfer_lname
    get_golfer_lname.short_description = 'Last name'
    get_golfer_lname.admin_order_field = 'golfer__golfer_lname'

    def get_golfer_fname(self, obj):
        return obj.golfer.golfer_fname
    get_golfer_fname.short_description = 'First name'
    get_golfer_fname.admin_order_field = 'golfer__golfer_fname'


# Register your models here.
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentType, TournamentTypeAdmin)
admin.site.register(TournamentParticipant, TournamentParticipantAdmin)