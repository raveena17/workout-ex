from django import forms
from matplotlib.table import Table

from .models import Cvr


class DateInput(forms.DateInput):
    input_type = 'date'

#class TimeInput(forms.TimeInput):
 #   time_input_type = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))

class cvrTableForm(forms.ModelForm):
    class Meta:
        model = Cvr

        fields = ('id', 'project_name', 'client_name', 'visit_location', 'date_of_visit', 'comments',
                  'reason_for_visit', 'actions_taken_during_the_visit', 'next_plan_of_action',)


        # fields = ('id', 'project_name', 'client_name', 'visit_location', 'date_of_visit', 'arrival_time', 'departure_time', 'comments',
        #           'reason_for_visit', 'actions_taken_during_the_visit', 'next_plan_of_action',)


        Table.exclude = ('project_id',)
        widgets = {
            'date_of_visit': DateInput(),
            'comments': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'reason_for_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'actions_taken_during_the_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'next_plan_of_action': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            # 'arrival_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
            # 'departure_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
        }

#forms.TimeInput(format='%H:%M %p'),