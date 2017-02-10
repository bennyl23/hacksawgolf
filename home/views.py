from django.views.generic import TemplateView
from tournament.models import Tournament


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def current_tournament(self):
        return Tournament.objects.current_tournament()
