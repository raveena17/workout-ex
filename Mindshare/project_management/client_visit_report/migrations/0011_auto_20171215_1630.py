# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-15 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit_report', '0010_auto_20171215_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisitreport',
            name='client_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
    ]
