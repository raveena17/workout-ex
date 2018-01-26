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
from django.views.generic.edit import FormView
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
import datetime
from helpers import get_full_domain
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import settings
from netifaces import interfaces, ifaddresses, AF_INET
from django.template.loader import get_template
from emailmanager import send
from django.views.decorators.csrf import csrf_exempt

               

# @login_required
def report_details(request):
    if request.user.is_superuser:
        requestlist = ClientVisitReport.objects.all()     
        approvallist = None
    else:
        # requestlist = ClientVisitReport.objects.filter(Q(prepared_by = request.user.username) | Q(reporting_senior_name = request.user.id)).filter(is_approved = False)
        requestlist = ClientVisitReport.objects.filter(prepared_by = request.user.username)
        approvallist = ClientVisitReport.objects.filter(reporting_senior_name = request.user.id).filter(is_approved = False, is_rejected = False)
    return render(request, 'client_visit_report/Cvr_Table.html', {'requestlist': requestlist, 'approvallist':approvallist})


def table(request):
    cvr_table = CVRTable(ClientVisitReport.objects.all())
    RequestConfig(request).configure(cvr_table)
    return render(request, 'client_visit_report/table.html', {'table': cvr_table})


def post_new(request, id=None):
    print(request.user.username)
    client_visit_report = None
    if id:
        client_visit_report = get_object_or_404(ClientVisitReport, id=id)

    postlist = ClientVisitReport.objects.all()
    if request.POST:
        # import pdb;pdb.set_trace()
        if request.POST['object']:
            cvr = get_object_or_404(ClientVisitReport, id=request.POST['object'])
            cvr.project_name = Project.objects.get(id=int(request.POST['project_name']))
            cvr.client_name = UserProfile.objects.get(id=request.POST['client_name'])
            cvr.visit_location = request.POST['visit_location']
            day, month, year = request.POST['date_of_visit'].split("-")
            visit_date = year +"-" +day+"-"+month
            cvr.date_of_visit = visit_date
            # cvr.arrival_time = request.POST['arrival_time']
            # cvr.departure_time = request.POST['departure_time']
            cvr.reason_for_visit = request.POST['reason_for_visit']
            cvr.actions_taken_during_the_visit = request.POST['actions_taken_during_the_visit']
            cvr.next_plan_of_action = request.POST['next_plan_of_action']
            cvr.comments = request.POST['comments']
            cvr.reporting_senior_name = User.objects.get(id=request.POST['reporting_senior_name'])
            cvr.save()


        # form = CvrTableForm(request.POST, instance=cvr)
        form = CvrTableForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.prepared_by = request.user.username 
            report.save()
        return redirect('/clientvisitreports/')

    else:
        form = CvrTableForm()
    project_name  = Project.objects.all()
    client_name = UserProfile.objects.filter(type='CC')
    reporting_senior_name = User.objects.filter(groups__name = 'Manager', is_active=True).exclude(username = request.user.username)

    context = {
        'form': form,
        'project_names':project_name,
        'client_names': client_name,
        'reporting_senior_names':reporting_senior_name
        #'action': 'Submit'
    }
    return render(request, "client_visit_report/Cvr_Form.html", context, {'some_flag': True})


@login_required
def view_cvr_report(request, id=None):
    # import pdb;pdb.set_trace()
    client_visit_report = ClientVisitReport.objects.get(id=id)
    obj = model_to_dict(client_visit_report)
    # import pdb;pdb.set_trace() 
    # print obj
    form = CvrTableForm(request.POST, initial=obj)
    project_name  = Project.objects.all()
    client_name = UserProfile.objects.filter(type='CC')
    reporting_senior_name = User.objects.filter(groups__name = 'Manager', is_active=True)
    # print obj['project_name']
    print obj['reporting_senior_name']
    context = {
        'form': form,
        'object':obj,
        'project':obj['project_name'],
        'client':obj['client_name'],
        'approve':obj['reporting_senior_name'],
        'project_names':project_name,
        'client_names': client_name,
        'reporting_senior_names':reporting_senior_name,
        # 'action': 'Submit'
    }
    return render(request, "client_visit_report/Cvr_Form.html", context)


def send_cvrreport_mail(sender, instance=None, created=False, update_fields=None, **kwargs):
    # import pdb;pdb.set_trace()
    if update_fields and 'is_approved' in update_fields:
        pass
    else:
        user = User.objects.get(username=instance.prepared_by)
        reporting_senior = User.objects.get(username=instance.reporting_senior_name.username)
        address = [i['addr'] for i in ifaddresses('enp4s0').setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        recipient, _ = get_user_model().objects.get_or_create(email=reporting_senior.email, first_name=reporting_senior.first_name, username=reporting_senior.username)                                    #http://127.0.0.1:8000/cvr/edit/id_num
        sender, _ = get_user_model().objects.get_or_create(email=user.email, first_name=user.first_name, username=user.username)
        subject = "Approve CVR form"

        template = get_template('client_visit_report/email/cvr_approval.txt')

        text_body = template.render({
            'client_visit_report': instance,
            'recipient': recipient,
            'reporting_senior_name':reporting_senior,
            'full_domain': "http://"+address[0]+":8000/clientvisitreports/report/" + str(instance.id)+"/",
            'request_user':instance.prepared_by
        })
        global send
        status = send(recipient, sender, subject, text_body)
        print status
models.signals.post_save.connect(send_cvrreport_mail, sender=ClientVisitReport)


def send_cvr_approval_mail(request, id):
    # import pdb;pdb.set_trace()
    cvr = ClientVisitReport.objects.get(id = int(id))
    user1 = User.objects.get(username=cvr.prepared_by)
    cvr.is_approved = True
    cvr.date_of_approval = datetime.datetime.now()
    cvr.save(update_fields=['is_approved', 'date_of_approval'])
    # cvr.save(update_fields=['is_approved'])
    subject = 'Approved CVR'
    message = "Dear {0}\n\nYour client visit report has been approved on {1}.\n\nRegrads\n{2}" .format(cvr,datetime.datetime.now(),request.user.username)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user1.email], fail_silently=False)
    return redirect("/clientvisitreports/")


def send_cvr_reject_mail(request, id):
    # import pdb;pdb.set_trace()
    cvr = ClientVisitReport.objects.get(id = int(id))
    user1 = User.objects.get(username=cvr.prepared_by)
    cvr.is_rejected = True
    cvr.date_of_approval = datetime.datetime.now()
    cvr.save()
    subject = 'Approve Rejected to clent visit report'
    message = "Dear {0}\n\nYour client visit report has been rejected.\n\nRegrads\n{1}" .format(cvr,request.user.username)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user1.email], fail_silently=False)
    return redirect("/clientvisitreports/")



@login_required
@csrf_exempt
def add_task_to_task_pane(request):
    result = []
    project_id = request.POST.get('project', None)
    if request.method == 'POST':
        form = TaskSelectionForm(request.POST,
                                 project=project_id, user=request.user)
        if form.is_valid():
            tasks = cache_tasks(request.user, form.cleaned_data['tasks'])
            map(lambda task: result.append({'id': task.pk,
                                            'name': unicode(task.project.name if task.project else
                                                            'Non Project Task') + ' : ' + unicode(task.name)}),
                Task.objects.filter(id__in=tasks))
            # return HttpResponse(simplejson.dumps(result),
            #                     mimetype='application/json')
            return HttpResponse(simplejson.dumps(result),
                                content_type='application/json')
        return HttpResponse(status=403)
    else:
        form = TaskSelectionForm(user=request.user)
    return render(request, 'add_task_to_task_pane.html', {'form': form})












# @receiver(post_save, sender=ClientVisitReport)
# def send_cvrreport_mail(sender, instance, created, **kwargs):
#     user = User.objects.get(username=instance.prepared_by)
#     if created:
#         link = "<a href=\"http://localhost:8000/clientvisitreport/clientvisitreports/" + str(instance.id) + "\" />"
#         sender= get_user_model().objects.get_or_create(email=user.email, first_name=user.first_name, username=user.username)
#         subject, to = 'Hello',  'raveena@5gindia.net'
#         text_content = 'Please refer my client visit report form.'
#         html_content = "<a href=\"http://localhost:8000/clientvisitreport/clientvisitreports/" + str(instance.id) + "\">link</a>"
#         msg = EmailMultiAlternatives(subject, text_content, sender, [to])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()