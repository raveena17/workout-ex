import string
from django import forms
from project_management.projects.models import Project, ProjectMembership, \
    DevelopmentProcess, DevelopmentEntity, ProjectRole
from django.contrib.auth.models import User
#from project_management.access_control.models import Role
from datetime import datetime

DATE_INPUT_FORMAT = '%m-%d-%Y'
default_date = datetime(1900, 0o1, 0o1).date()


class InitiationForm(forms.ModelForm):
    approval_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        disable_fields = kwargs.pop('disabled', False) if kwargs else False
        instance = kwargs['instance']
        super(InitiationForm, self).__init__(*args, **kwargs)
        if instance and instance.id:
            self.fields['approval_date'].initial = instance.schedules.approval_date
        if disable_fields:
            for field in self.fields.itervalues():
                field.widget.attrs['disabled'] = True

    class Meta:
        model = Project
        fields = ('name', 'apex_body_owner', 'business_unit', 'owner',
                  'domain', 'project_type', 'customer', 'planned_effort',
                  'approval_type')


date_fields = ('planned_start_date', 'planned_end_date',
               'actual_start_date', 'actual_end_date')


class PlanForm(forms.ModelForm):
    planned_start_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                         required=False)
    planned_end_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                       required=False)
    actual_start_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                        required=False)
    actual_end_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                      required=False)
    development_process = forms.ModelChoiceField(
        DevelopmentProcess.objects.all(), empty_label='Select',
        required=False)

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['development_environment'].queryset = \
                instance.development_environment.all()
            for date in date_fields:
                date_value = getattr(instance.schedules, date)
                if date_value != default_date:
                    self.fields[date].initial = date_value

    def save(self, force_insert=False, force_update=False, commit=True):
        project = super(PlanForm, self).save(commit=False)
        for field_name in date_fields:
            setattr(project.schedules, field_name,
                    self.cleaned_data[field_name])
        if commit:
            project.schedules.save()
            project.save()
        return project

    class Meta:
        model = Project
        fields = date_fields + ('objective', 'goals', 'project_scope',
                                'development_process', 'development_environment')


def make_responsibility_form(project=None):
    """
        (Factory) Make form for project responsibilities for specified project.
        The roles in a project typically are 'technical_leads', 'quality_leads',
        'developers', 'testers', 'technical_writers', 'configuration_manager',
        'release_manager', 'process_auditors', 'change_control_board'.
    """
    if not project:
        raise NameError('Project is not defined. Unable to create form.')
    choices = User.objects.filter(
        is_active=True).filter(
        is_staff=False).order_by('username')
    roles = ProjectRole.objects.all()

    def invert_dict(d):
        """ Invert a dict's keys and values. """
        new_dict = {}
        for k in d:
            for v in d[k]:
                new_dict.setdefault(v, []).append(k)
        return new_dict

    def get_responsibility_set():
        """ Returns a dict of people responsible for project specific roles. """
        responsibility_set = {}
        for role in roles:
            responsibility_set[role.group.name.replace(' ', '_')] = [pm.member.pk
                                                                     for pm in role.group.projectmembership_set.filter(project=project)]
        return responsibility_set

    def make_choice_fields(role):
        return forms.ModelMultipleChoiceField(queryset=choices, required=False)

    def make_fieldnames(role):
        return role.group.name.replace(' ', '_')

    def __init__(self, *args, **kwargs):
        """
            __init__ method of the dynamic form.
        """
        if 'data' not in kwargs:
            kwargs['data'] = get_responsibility_set()
        super(self.__class__, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True):
        """
            Save method of the dynamic form.
        """
        responsiblity_set = invert_dict(self.cleaned_data)
        project.projectmembership_set.exclude(roles=None).delete()
        for user, role_names in responsiblity_set.items():
            membership = ProjectMembership(project=project, member=user)
            membership.save()
            for name in role_names:
                role = ProjectRole.objects.get(
                    group__name__exact=string.capwords(name.replace('_', ' ')))
                membership.roles.add(role.group)
        return project

    properties = dict(zip(map(make_fieldnames, roles) + ['project', '__init__', 'save'],
                          map(make_choice_fields, roles) + [project, __init__, save]))

    return type('ResponsibilityForm', (forms.Form,), properties)


class DevelopmentEnvironmentForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = DevelopmentEntity
