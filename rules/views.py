from django.views.generic import TemplateView
from rules.models import Rule


class RuleView(TemplateView):
    template_name = 'rules/rules.html'

    def rule(self):
        qRule = Rule.objects.all()
        return qRule[0]