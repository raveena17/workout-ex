# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-08 17:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientVisitReport',
        ),
    ]