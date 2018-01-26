# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-07 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientVisitReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prepared_by', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('client_name', models.CharField(max_length=200)),
                ('visit_location', models.CharField(max_length=200)),
                ('date_of_visit', models.DateField(blank=True, null=True)),
                ('arrival_time', models.TimeField(null=True)),
                ('departure_time', models.TimeField(null=True)),
                ('approved_by', models.CharField(max_length=200)),
                ('date_of_approval', models.DateTimeField(blank=True, null=True)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('reason_for_visit', models.TextField(blank=True, max_length=200, null=True)),
                ('actions_taken_during_the_visit', models.TextField(blank=True, max_length=200, null=True)),
                ('next_plan_of_action', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
