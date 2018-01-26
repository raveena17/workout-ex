from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import IntegrityError

from django.shortcuts import redirect
from django_tables2 import RequestConfig
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CvrTableForm
from .tables import CVRTable
from .models import ClientVisitReport
from project_management.projects.models import *
from project_management.users.models import *
from django.contrib.auth.models import User, Group

               
# @login_required
def manage_cvr_initiation_request(request):
    return render(request, 'cvr/Cvr_Form.html')

def table(request):
    # import pdb;pdb.set_trace()

    cvr_table = CVRTable(ClientVisitReport.objects.all())
    RequestConfig(request).configure(cvr_table)
    return render(request, 'cvr/table.html', {'table': cvr_table})


# def table_list(request):
#     postlist = ClientVisitReport.objects.all()
#     context = {'postlist': postlist}
#     return render(request, 'table_list.html', {'postlist': postlist})


#@login_required
def post_new(request):
    print(request.user.username)
    postlist = ClientVisitReport.objects.all()
    print postlist
    if request.POST:
        form = CvrTableForm(request.POST)
        report = ClientVisitReport(
            prepared_by = request.user.username,
            project_name = Project.objects.get(id=request.POST.get('Project Name')),           #Forignkey
            client_name = UserProfile.objects.get(id=request.POST.get('Client Name')),
            visit_location = request.POST["location"],
            date_of_visit = request.POST["date_of_visit"],
            arrival_time = request.POST["arrival_time"],
            departure_time = request.POST["departure_time"],
            comments = request.POST["comments"],
            reason_for_visit = request.POST["reason_for_visit"],
            actions_taken_during_the_visit = request.POST["actions"],
            next_plan_of_action = request.POST["next_action"],
            reporting_senior_name = User.objects.get(id=request.POST.get('Reporting Senior Name')))
            # date_of_approval = request.POST["date_of_approval"])
        report.save()
        return redirect('/client_visit_report/')

    else:
        form = CvrTableForm()
    project_name  = Project.objects.all()
    client_name = UserProfile.objects.filter(type='CC')
    reporting_senior_name = User.objects.filter(groups__name = 'Manager', is_active=True)

    context = {
        'form': form,
        'project_names':project_name,
        'client_names': client_name,
        'reporting_senior_names':reporting_senior_name,
        # 'user_names':approved_by,
        'action': 'Submit'
    }

    return render(request, "cvr/Cvr_Form.html", context)


def view_cvr_list(request):
    postlist = ClientVisitReport.objects.all()

    context = {'postlist': postlist} 
    return render(request, 'cvr/report_details.html', {'postlist': postlist})


def delete_cvr_report(request):
    _id = request.GET['id']
    clientvisitreport = ClientVisitReport.objects.get(pk=_id)
    clientvisitreport.delete()
    return HttpResponse(clientvisitreport.project_name + "   " + "record deleted")



class CvrUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientVisitReport
    form_class = CvrTableForm

    def get_success_url(self):
        # This will be a different view
        return reverse('table')

    def get_context_data(self, **kwargs):
        context_data = super(CvrUpdateView, self).get_context_data(**kwargs)
        context_data['action'] = 'Approve'
        return context_data

    def post(self, request, *args, **kwargs):
        result = super(CvrUpdateView, self).post(request, *args, **kwargs)
        print(self.object)
        if self.object:
            self.object.approved_by = request.user.username
            self.object.date_of_approval = timezone.now()
            self.object.save()
        return result


@login_required
# @csrf_token
def list(request):
    query = Q()
    search_text = request.GET.get('search', '')
    if search_text:
        q = Q()
        for term in search_text.split():
            q = Q(name__icontains=term)
        query = query & q
    task_set = ClientVisitReport.objects.filter(query).filter(
        project_name=None).filter(
        status=None).filter(
            priority=None)
    callable = SubListView.as_view(
        queryset=task_set,
        template_name="list.html",
        context_object_name="task_list",
        paginate_by=20
    )
    return callable(request)


# @login_required
# def manage_non_project_task(request, id=None):
#     """
#         Add/Edit non project task.
#     """
#     non_project_task = None
#     if id:
#         non_project_task = get_object_or_404(Task, pk=id)
#     if request.method == 'POST':
#         form = NonProjectTaskForm(request.POST, instance=non_project_task)
#         if form.is_valid():
#             form.save(user=request.user)
#             messages.success(
#                 request, _('Non Project Task saved successfully.'))
#             return HttpResponseRedirect(reverse(non_project_task_list))
#     else:
#         form = NonProjectTaskForm(instance=non_project_task)
#     return render(request, 'non_project_task.html', {'form': form},
#                   )


@login_required
def delete(request, is_project_task=False):
    """
        Delete project/non-project-task task.
    """
    task_id = request.POST.getlist('task_pk')
    print task_id
    for i in task_id:
        val_check = ClientVisitReport.objects.filter(task=i)
        if len(val_check) == 0:
            Task.objects.filter(pk__in=task_id).delete()
            messages.success(request, _('Task(s) deleted successfully.'))
        else:
            messages.error(
                request,
                _('Task used in Timesheet, Unable to delete this Task'))
    if is_project_task:
        RedirectView = reverse(task_list) + '?pid=' \
            + request.GET.get('pid', '')
    else:
        RedirectView = reverse(non_project_task_list)
    return HttpResponseRedirect(RedirectView)