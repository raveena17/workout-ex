from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import IntegrityError

from django.shortcuts import redirect
from django_tables2 import RequestConfig
# from django.core.context_processors import csrf
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
# from project_management.customer.models import *
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

#@login_required
def post_new(request):
    print(request.user.username)

    if request.POST:
        form = CvrTableForm(request.POST)
        if form.is_valid():
            cvr_item = form.save(commit=False)
            cvr_item.prepared_by = request.user.username #change it for request user
            cvr_item.save()
            return redirect(reverse('table'))
            # return redirect('table')
        # return redirect(reverse('post_new'))
        # return redirect('post_new')

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

















# #helper
# #@login_required
# def post_new(request):
#     print(request.user.username)
    
#     if request.POST:
#         # import pdb;pdb.set_trace()

#         form = CvrTableForm(request.POST)
#         report = ClientVisitReport(
#             prepared_by = request.user.username,
#             project_name = Project.objects.get(id=request.POST.get('Project Name')),
#             client_name = UserProfile.objects.get(id=request.POST.get('Client Name')),
#             visit_location = request.POST["location"],
#             date_of_visit = request.POST["date_of_visit"],
#             arrival_time = request.POST["arrival_time"],
#             departure_time = request.POST["departure_time"],
#             comments = request.POST["comments"],
#             reason_for_visit = request.POST["reason_for_visit"],
#             actions_taken_during_the_visit = request.POST["actions"],
#             next_plan_of_action = request.POST["next_action"],
#             reporting_senior_name = User.objects.get(id=request.POST.get('Reporting Senior Name')))
#             # date_of_approval = request.POST["date_of_approval"])
#         # print report
#         report.save()
#         return redirect('table_list')