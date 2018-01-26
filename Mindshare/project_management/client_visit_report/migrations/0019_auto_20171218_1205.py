# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-18 12:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0018_auto_20171218_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_visit_report_clientvisitreport_approved_by', to=settings.AUTH_USER_MODEL, verbose_name='Request To'),
        ),
    ]