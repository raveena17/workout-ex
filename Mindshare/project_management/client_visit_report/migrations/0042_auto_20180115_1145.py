# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-15 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0041_auto_20180112_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='arrival_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='clientvisitreport',
            name='departure_time',
            field=models.TimeField(null=True),
        ),
    ]
