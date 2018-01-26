from django.conf.urls import url
from project_management.client_visit_report.views import *

app_name = 'client_visit_report'
urlpatterns = [

    url(r'^$', report_details),
    url(r'^sample_table$',table, name='table'),
    url(r'^create/$', post_new, name='post_new'),
    url(r'^report/(?P<id>\d+)/$', view_cvr_report),
    url(r'^request/$', send_cvrreport_mail),
    url(r'^approve/(?P<id>\d+)/$', send_cvr_approval_mail),
    url(r'^reject/(?P<id>\d+)/$', send_cvr_reject_mail),

    
    url(r'addtask/$', add_task_to_task_pane),





    # url(r'^request/(?P<id>\d+)/$', manage_cvr_initiation_request),
    # url(r'^update/(?P<id>\d+)/$', CvrUpdateView.as_view()),
    # url(r'^edit/(?P<pk>\d+)/$', CvrUpdateView.as_view(), name='edit_cvr'),
    # url(r'^clientvisitreports/$', ClientVisitReportList.as_view(), name="clientvisitreport-list"),    
    # url(r'^clientvisitreports/create/$', ClientVisitReportCreate.as_view(), name="clientvisitreport-create"),    
    # url(r'^clientvisitreports/(?P<pk>[0-9]+)/$', ClientVisitReportUpdate.as_view(), name='clientvisitreport-update')

]
