# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-21 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0031_auto_20171221_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientvisitreport',
            old_name='reporting_senior',
            new_name='reporting_senior_name',
        ),
    ]