# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-15 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0009_auto_20171215_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='client_name',
            field=models.CharField(max_length=200),
        ),
    ]
