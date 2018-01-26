from __future__ import unicode_literals
from django.db import models
import datetime
from project_management.users.models import UserProfile
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from emailmanager import send
from helpers import get_full_domain
from project_management.projects.models import *
from project_management.users.models import *
from django.contrib.auth.models import User, Group
from django.urls import reverse 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives



class ClientVisitReport(models.Model):

    prepared_by = models.CharField(max_length=200, blank=False, null=False)#foriegn key to the user
    project_name = models.ForeignKey(Project, verbose_name=('project name'), default=None, null=True)
    client_name = models.ForeignKey(UserProfile,
                                         verbose_name=('Client Details'), default=None, null=True, blank=True)
    visit_location = models.CharField(max_length=200, blank=False, null=False)
    date_of_visit = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    comments = models.TextField(max_length=200, blank=True, null=True)
    reason_for_visit = models.TextField(max_length=200, blank=True, null=True)
    actions_taken_during_the_visit = models.TextField(max_length=200, blank=True, null=True)
    next_plan_of_action = models.TextField(max_length=200, blank=True, null=True)
    comments = models.TextField(max_length=200, blank=True, null=True)
    reporting_senior_name = models.ForeignKey(User, default=None, blank=True, null=True, verbose_name=('reporting_senior_name'), related_name="%(app_label)s_%(class)s_reporting_senior_name")
    reason_for_reject = models.TextField(max_length=200, blank=True, null=True)
    date_of_approval = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default =False)
    is_rejected = models.BooleanField(default =False)


    def __str__(self):
        return self.prepared_by 

    def get_absolute_url(self):
        return reverse('cvr-detail', kwargs={'pk': self.pk})


    class Meta:
       db_table = 'ClientVisitReport'
       verbose_name_plural = "clientvisitreports"






#code for send Email to link

# @receiver(post_save, sender=ClientVisitReport)
# def onSave(sender, instance, created, **kwargs):
#     user = User.objects.get(username=instance.prepared_by)
#     if created:
        # link = "<a href=\"http://localhost:8000/client_visit_report/clientvisitreports/" + str(instance.id) + "\" />"
#         sender= get_user_model().objects.get_or_create(email=user.email, first_name=user.first_name, username=user.username)
#         subject, to = 'Hello',  'raveena@5gindia.net'
#         text_content = 'Please refer my client visit report form.'
        # html_content = "<a href=\"http://localhost:8000/client_visit_report/clientvisitreports/" + str(instance.id) + "\">link</a>"
#         msg = EmailMultiAlternatives(subject, text_content, sender, [to])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()