# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-06 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0038_auto_20180104_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='arrival_time',
            field=models.TimeField(default='00:00', null=True),
        ),
        migrations.AlterField(
            model_name='clientvisitreport',
            name='departure_time',
            field=models.TimeField(default='00:00', null=True),
        ),
    ]