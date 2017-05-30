from django import forms
from register.models import User


# custom model choice field to display user_team_name as the display in the dropdown
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.user_team_name


class TeamCompareForm(forms.Form):

    team_one_compare = UserModelChoiceField(
        label='Team 1',
        queryset=User.objects.all().order_by('user_team_name'),
        to_field_name='user_id',
        empty_label='Select team 1',
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )
    team_two_compare = UserModelChoiceField(
        label='Team 2',
        queryset=User.objects.all().order_by('user_team_name'),
        to_field_name='user_id',
        empty_label='Select team 2',
        widget=forms.Select(
            attrs={'class':'form-control', 'autofocus':'autofocus'}
        )
    )



