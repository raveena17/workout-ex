# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-23 10:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0051_clientvisitreport_reason_for_reject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientvisitreport',
            name='reason_for_reject',
        ),
    ]