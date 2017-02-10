from django.contrib import admin
from golfer.models import Golfer
from tournament.models import TournamentParticipant


# custom golfer filter to see who has or has not been a tournament participant
class GolferHasPlayedFilter(admin.SimpleListFilter):
    parameter_name = 'has_played'
    title = 'Has played'
    YES = 'has_played'
    NO = 'has_not_played'

    def lookups(self, request, model_admin):
        return (
                (self.YES, 'Yes'),
                (self.NO, 'No'),
        )

    def queryset(self, request, queryset):
        # get a queryset of distinct golfer_id's from the TournamentParticipant table
        q_golfer_id_has_played = TournamentParticipant.objects.order_by('golfer_id').values('golfer_id').distinct()
        # convert the queryset into a list to use in the filters
        lst_golfer_id_has_played = q_golfer_id_has_played.values_list('golfer_id', flat=True)

        if self.value() == self.YES:
            return queryset.filter(golfer_id__in=lst_golfer_id_has_played)
        if self.value() == self.NO:
            return queryset.exclude(golfer_id__in=lst_golfer_id_has_played)

        return queryset


class GolferAdmin(admin.ModelAdmin):
    fields = ['golfer_fname', 'golfer_lname', 'golfer_mi', 'default_salary', 'original_salary']
    list_display = ['golfer_lname', 'golfer_fname', 'default_salary', 'original_salary']
    list_editable = ['default_salary', 'original_salary']
    list_per_page = 10000
    ordering = ('golfer_lname', 'golfer_fname')
    list_filter = [GolferHasPlayedFilter]


admin.site.register(Golfer, GolferAdmin)
