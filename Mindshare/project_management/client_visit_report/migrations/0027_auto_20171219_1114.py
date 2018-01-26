# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-19 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0026_auto_20171219_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='client_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='Client Details'),
        ),
    ]
