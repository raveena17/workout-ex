# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-21 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0032_auto_20171221_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='reporting_senior_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='reporting_senior_name'),
        ),
    ]
