# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-21 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0035_auto_20171221_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientvisitreport',
            name='reporting_senior',
        ),
    ]
