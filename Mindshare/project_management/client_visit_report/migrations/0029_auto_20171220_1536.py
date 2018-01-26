# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-20 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0028_auto_20171219_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_visit_report_clientvisitreport_approved_by', to='users.UserProfile', verbose_name='Request To'),
        ),
        migrations.AlterField(
            model_name='clientvisitreport',
            name='client_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.CustomerContact', verbose_name='client name'),
        ),
        migrations.AlterField(
            model_name='clientvisitreport',
            name='project_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='project name'),
        ),
    ]