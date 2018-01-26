from django import forms
from matplotlib.table import Table
from django import forms
from django.contrib.auth.models import User, Group
from .models import ClientVisitReport
from project_management.projects.models import *

class DateInput(forms.DateInput):
    input_type = 'date'


# class CvrTableForm(forms.ModelForm):

#     class Meta:
#         model = ClientVisitReport
#         fields = "__all__"


class CvrTableForm(forms.ModelForm):
    project_name = Project.objects.all()
    def __init__(self, *args, **kwargs):    
        super(CvrTableForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields['project_name'].queryset=Project.objects.all()
            self.fields['project_name'].initial = self.initial['project_name']
            # self.fields['client_name'].queryset=UserProfile.objects.filter(type='CC')
            # self.fields['client_name'].initial = self.initial['client_name']



    class Meta:
        model = ClientVisitReport
        # fields = "__all__"

        fields = ('project_name', 'client_name', 'visit_location', 'date_of_visit', 'arrival_time', 'departure_time', 'comments',
                  'reason_for_visit', 'actions_taken_during_the_visit', 'next_plan_of_action','reporting_senior_name','reason_for_reject')

        Table.exclude = ('project_id',)
        widgets = {
            'date_of_visit': DateInput(),
            'comments': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'reason_for_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'actions_taken_during_the_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'next_plan_of_action': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'arrival_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
            'departure_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
        }


class TaskSelectionForm(forms.Form):
    {
        
    }

    # def __init__(self, *args, **kwargs):    
    #     super(CvrTableForm, self).__init__(*args, **kwargs)


        # if kwargs.has_key('instance'):
        #     instance = kwargs['instance']
        #     self.fields['visit_location'].initial = instance.visit_location
        #     print self.initial['visit_location']



    # def __init__(self, *args, **kwargs):    
    #     super(CvrTableForm, self).__init__(*args, **kwargs)
    #     self.fields['visit_location'].initial=self.initial['visit_location']
    #     print self.fields['visit_location']
    #     if self.initial !='':
    #         self.fields['project_name'].initial=self.initial['project_name']