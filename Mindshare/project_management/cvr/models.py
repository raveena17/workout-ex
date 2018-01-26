# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.template.loader import get_template
from emailmanager import send
from helpers import get_full_domain




# def email_manager(sender, instance=None, created=False, **kwargs):
#     if created:
#         # Get the sender and recipient from the instance
#         recipient, _ = get_user_model().objects.get_or_create(email="thiyanithi@5gindia.net", first_name="thiyanithi", username="thiyanithi")
#         sender, _ = get_user_model().objects.get_or_create(email="raveena@5gindia.net", first_name="raveenapriya", username="raveenapriya")
#         # recipient, _ = get_user_model().objects.get_or_create(email="test@test.com", first_name="test", username="test")
#         # sender, _ = get_user_model().objects.get_or_create(email="sender@test.com", first_name="sender", username="sender")
#         subject = "Please refer to my CVR form"
#         template = get_template('cvr/email/cvr_approval.txt')
#         text_body = template.render({
#             'cvr': instance,
#             'recipient': recipient,
#             'full_domain': get_full_domain()
#         })
#         status = send(recipient, sender, subject, text_body)
#         print status



class Cvr(models.Model):
    prepared_by = models.CharField(max_length=200, blank=False, null=False)
    # prepared_by = models.ForeignKey()#foriegn key to the user
    project_name = models.CharField(max_length=200, blank=False, null=False)
    client_name = models.CharField(max_length=200, blank=False, null=False)
    visit_location = models.CharField(max_length=200, blank=False, null=False)
    date_of_visit = models.DateField(null=True, blank=True)
    # arrival_time = models.TimeField(null=True)
    # departure_time = models.TimeField(null=True)
    # approved_by should be a ForeignKey to a user
    approved_by = models.CharField(max_length=200, blank=False, null=False)
    date_of_approval = models.DateTimeField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    reason_for_visit = models.CharField(max_length=200, blank=True, null=True)
    actions_taken_during_the_visit = models.CharField(max_length=200, blank=True, null=True)
    next_plan_of_action = models.CharField(max_length=200, blank=True, null=True)





# models.signals.post_save.connect(email_manager, sender=Cvr)
